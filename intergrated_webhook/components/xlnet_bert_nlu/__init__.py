from rasa.nlu.components import Component
import typing
from typing import Any, Optional, Text, Dict

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata

import os, sys, time
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
import utils.vocab_reader as vocab_reader
import models.slot_tagger as slot_tagger
import models.snt_classifier as snt_classifier
import torch
from pytorch_transformers import BertTokenizer, BertModel, XLNetTokenizer, XLNetModel 
from utils.bert_xlnet_inputs import prepare_inputs_for_bert_xlnet

import itertools
import numpy as np
import re


emb_size = None
hidden_size = 200 # 100, 200 
bidirectional = True
num_layers = 1
dropout = 0.1 # 0.1, 0.5 
multiClass = False
encoder_info_filter = lambda info: info
fix_pretrained_model = False

class LangModel(object):
    def __init__(self):
        self.tag_to_idx = {}
        self.idx_to_tag = {}
        self.class_to_idx = {}
        self.idx_to_class = {}
        self.tokenizer = None
        self.model_class = None
        self.model_tag = None

    

class XlnetBertNLU(Component):
    name = "xlnet_bert_nlu"
    provides = ["intent", "entities"]
    requires = ["tokens"]
    defaults = {}
    language_list = ["en", "vi", "jp"]

    def load_model(self, lang, tag_to_idx, class_to_idx):
        if lang in ['ja']:
            pretrained_model_name = "bert-base-multilingual-uncased"
        else:
            pretrained_model_name = "bert-base-uncased"
        MODEL_CLASSES = {
            'bert': (BertModel, BertTokenizer),
            'xlnet': (XLNetModel, XLNetTokenizer),
        }
        pretrained_model_class, tokenizer_class = MODEL_CLASSES[self.pretrained_model_type]
        tokenizer = tokenizer_class.from_pretrained(pretrained_model_name)

        if fix_pretrained_model:
            pretrained_model = pretrained_model_class.from_pretrained(pretrained_model_name, output_hidden_states = True)
        else:
            pretrained_model = pretrained_model_class.from_pretrained(pretrained_model_name)

        model_tag = slot_tagger.LSTMTagger(emb_size, hidden_size, None, len(tag_to_idx), 
                                       bidirectional=bidirectional, 
                                       num_layers=num_layers, 
                                       dropout=dropout, 
                                       device=self.device, 
                                       pretrained_model=pretrained_model, 
                                       pretrained_model_type=pretrained_model_name, 
                                       fix_pretrained_model=fix_pretrained_model)

        model_class = snt_classifier.sntClassifier_hiddenAttention(hidden_size, len(class_to_idx), 
                                                               bidirectional=bidirectional, 
                                                               num_layers=num_layers, 
                                                               dropout=dropout, 
                                                               device=self.device, 
                                                               multi_class=multiClass)
        
        model_tag.load_model(os.path.join(self.model_dir, lang, 'model.tag'))
        model_class.load_model(os.path.join(self.model_dir, lang, 'model.class'))

        model_tag = model_tag.to(self.device)
        model_class = model_class.to(self.device)

        model_tag.eval()
        model_class.eval()

        return tokenizer, model_tag, model_class

    def load_lang_model(self, lang):
        lang_model = LangModel()
        lang_model.tag_to_idx, lang_model.idx_to_tag = vocab_reader.read_vocab_file(os.path.join(self.model_dir, lang, 'vocab.tag'), bos_eos=False, no_pad=True, no_unk=True)
        lang_model.class_to_idx, lang_model.idx_to_class = vocab_reader.read_vocab_file(os.path.join(self.model_dir, lang, 'vocab.class'), bos_eos=False, no_pad=True, no_unk=True)
        lang_model.tokenizer, lang_model.model_tag, lang_model.model_class = self.load_model(lang, lang_model.tag_to_idx, lang_model.class_to_idx)
        return lang_model

    def __init__(self, component_config=None):
        super(XlnetBertNLU, self).__init__(component_config)
        self.model_dir = os.path.join(os.path.dirname(__file__), "model")
        self.device = torch.device("cpu")
        self.pretrained_model_type = "bert" # bert, xlnet

        self.ja_model = self.load_lang_model('ja')
        self.vi_model = self.load_lang_model('vi')
        self.en_model = self.load_lang_model('en')

    def train(self, training_data, cfg, **kwargs):
        pass

    def process(self, message, **kwargs):
        """Retrieve the tokens of the new message, pass it to the classifier
            and append prediction results to the message class."""

        tokens = [t.text for t in message.get("tokens")]
        if message.get("lang") in ['ja']:
            self.feed_model(self.ja_model, tokens, message)
        elif message.get("lang") in ['vi']:
            self.feed_model(self.vi_model, tokens, message)
        elif message.get("lang") in ['en']:
            self.feed_model(self.en_model, tokens, message)

    def feed_model(self, lang_model, tokens, message):
        inputs = prepare_inputs_for_bert_xlnet([tokens], [len(tokens)], lang_model.tokenizer, 
                    cls_token_at_end=bool(self.pretrained_model_type in ['xlnet']),  # xlnet has a cls token at the end
                    cls_token=lang_model.tokenizer.cls_token,
                    sep_token=lang_model.tokenizer.sep_token,
                    cls_token_segment_id=2 if self.pretrained_model_type in ['xlnet'] else 0,
                    pad_on_left=bool(self.pretrained_model_type in ['xlnet']), # pad on the left for xlnet
                    pad_token_segment_id=4 if self.pretrained_model_type in ['xlnet'] else 0,
                    device=self.device)

        tag_scores, encoder_info = lang_model.model_tag(inputs, [len(tokens)], with_snt_classifier=True)
        top_pred_slots = tag_scores.data.cpu().numpy().argmax(axis=-1)

        entities = []
        pre_entity = "O"
        entity_value = ""
        for idx, slot in enumerate(top_pred_slots[0]):
            entity = list(lang_model.tag_to_idx.keys())[list(lang_model.tag_to_idx.values()).index(slot)]
            if entity == pre_entity:
                entity_value += tokens[idx] + " "
            elif entity != pre_entity:
                if pre_entity != "O":
                    entities.append({
                        "value" : entity_value.rstrip(),
                        "entity" : pre_entity
                    })
                entity_value = tokens[idx] + " "
                pre_entity = entity

        if pre_entity != "O":
            entities.append({
                "value" : entity_value.rstrip(),
                "entity" : pre_entity
            })
        self.compose_entities(entities, message.get("lang"))
        message.set("entities", message.get("entities", []) + entities)

        class_scores = lang_model.model_class(encoder_info_filter(encoder_info))
        snt_probs = class_scores.data.cpu().numpy()

        intent = {"name": lang_model.idx_to_class[snt_probs.argmax(axis=-1)[0]], "confidence": float(np.exp(snt_probs.max(axis=-1))[0])}
        message.set("intent", intent, add_to_output=True)

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this component to disk for future loading."""
        pass

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        model_metadata: Optional["Metadata"] = None,
        cached_component: Optional["Component"] = None,
        **kwargs: Any
    ) -> "Component":
        """Load this component from file."""
        if cached_component:
            return cached_component
        else:
            return cls(meta)

    def compose_entities(self, entities, lang):
        self.begin_entity = False
        composed_entity = None
        for entity in entities:
            entity_value = str(entity["value"])
            entity_name = str(entity["entity"])
            if re.match(r"I-(.*)", entity_name):
                if self.begin_entity:
                    if lang in ['ja', 'zh-cn', 'zh']:
                        composed_entity["value"] = str(composed_entity["value"]) + entity_value
                    else:
                        composed_entity["value"] = str(composed_entity["value"]) + " " + entity_value
                else:
                    composed_entity = None
                entities.remove(entity)
            elif re.match(r"B-(.*)", entity_name):
                self.begin_entity = True
                composed_entity = entity
                composed_entity["entity"] = composed_entity["entity"][2:]
                entities.remove(entity)
                continue
            elif self.begin_entity and composed_entity is not None:
                entities.append(composed_entity)
                self.begin_entity = False
                composed_entity = None

        if self.begin_entity and composed_entity is not None:
            entities.append(composed_entity)