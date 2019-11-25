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
from pytorch_transformers import BertTokenizer, BertModel, XLNetTokenizer, XLNetModel , DistilBertTokenizer, DistilBertModel
from utils.bert_xlnet_inputs import prepare_inputs_for_bert_xlnet

import itertools
import numpy as np
import re
from .slot_nlu_train import SlotNluTrain
from rasa.nlu.training_data.training_data import TrainingData
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import json

emb_size = None
hidden_size = 100 # 100, 200 
bidirectional = True
num_layers = 1
dropout = 0.1 # 0.1, 0.5 
multiClass = False
encoder_info_filter = lambda info: info
fix_pretrained_model = False

configPath = os.path.join(os.path.dirname(__file__), "..", "..")
def getLangFromConfig():
    configFile = os.path.join(configPath, "config.json")
    with open(configFile, "r+") as jsonFile:
        data = json.load(jsonFile)
        return data["lang"]

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
    language_list = ["vi", "en", "ja"]

    def load_model(self, lang, tag_to_idx, class_to_idx):
        # if lang in ['ja']:
        #     pretrained_model_name = "bert-base-multilingual-uncased"
        # else:
        #     pretrained_model_name = "bert-base-uncased"
        pretrained_model_name = 'distilbert-base-uncased'
        MODEL_CLASSES = {
            'bert': (BertModel, BertTokenizer),
            'distil-bert': (DistilBertModel, DistilBertTokenizer),
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

    def on_modified(self, event):
        configLang = getLangFromConfig()
        self.nluModel = self.load_lang_model(configLang)

    def __init__(self, component_config=None):
        super(XlnetBertNLU, self).__init__(component_config)
        self.model_dir = os.path.join(os.path.dirname(__file__), "model")
        self.device = torch.device("cpu")
        self.pretrained_model_type = "distil-bert" # bert, xlnet, distil-bert
        self.intent_confidence = 0.3
        self.intent_unk = "<unk>"

        event_handler = PatternMatchingEventHandler(patterns=["*.json"],
                                    ignore_patterns=[],
                                    ignore_directories=True)
        event_handler.on_modified = self.on_modified
        observer = Observer()
        observer.schedule(event_handler, path=configPath, recursive=False)
        observer.start()

        try:
            configLang = getLangFromConfig()
            self.nluModel = self.load_lang_model(configLang)
        except OSError as e:
            print("Pass error : Please train this model before using - " + str(e))

    def train(self, training_data, cfg, **kwargs):
        multi_lang_training_data = self.splitMultiLang(training_data)
        for lang in multi_lang_training_data:
            lang_training_data = TrainingData(
                multi_lang_training_data[lang],
                entity_synonyms=training_data.entity_synonyms,
                regex_features=training_data.regex_features,
                lookup_tables=training_data.lookup_tables,
            )
            slotNluTrain = SlotNluTrain(lang_training_data, lang)
            slotNluTrain.train()

    def splitMultiLang(self, training_data):
        multi_lang_training_data = {}
        for example in training_data.training_examples:
            if example.get("lang") not in multi_lang_training_data:
                multi_lang_training_data[example.get("lang")] = [example]
            else:
                multi_lang_training_data[example.get("lang")].append(example)
        return multi_lang_training_data

    def process(self, message, **kwargs):
        """Retrieve the tokens of the new message, pass it to the classifier
            and append prediction results to the message class."""

        tokens = [t.text for t in message.get("tokens")]
        self.feed_model(self.nluModel, tokens, message)

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
        lang = message.get("lang")
        for idx, slot in enumerate(top_pred_slots[0]):
            entity = list(lang_model.tag_to_idx.keys()) [list(lang_model.tag_to_idx.values()).index(slot)]
            if entity[2:] == pre_entity[2:]:
                if lang == "ja":
                    entity_value = entity_value + tokens[idx]
                else:
                    entity_value = entity_value + " " + tokens[idx]
            else:
                if pre_entity != "O":
                    entities.append({
                        "value" : entity_value.rstrip(),
                        "entity" : pre_entity
                    })
                entity_value = tokens[idx]
                pre_entity = entity


        if pre_entity != "O":
            entities.append({
                "value" : entity_value.rstrip(),
                "entity" : pre_entity
            })
        entities = self.compose_entities(entities, lang)
        message.set("entities", message.get("entities", []) + entities)

        class_scores = lang_model.model_class(encoder_info_filter(encoder_info))
        snt_probs = class_scores.data.cpu().numpy()
        
        confidence = float(np.exp(snt_probs.max(axis=-1))[0])
        if confidence < self.intent_confidence:
            intent_name = lang_model.idx_to_class[snt_probs.argmax(axis=-1)[0]]
            intent = {"name": self.intent_unk, "confidence": confidence, "cls_name": intent_name}
        else:
            intent = {"name": lang_model.idx_to_class[snt_probs.argmax(axis=-1)[0]], "confidence": confidence}

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
        composed_entities = []
        self.begin_entity = False
        composed_entity = None
        for entity in entities:
            entity_value = str(entity["value"])
            entity_name = str(entity["entity"])
            if re.match(r"I-(.*)", entity_name):
                if self.begin_entity:
                    if lang in ['ja']:
                        composed_entity["value"] = str(composed_entity["value"]) + entity_value
                    else:
                        composed_entity["value"] = str(composed_entity["value"]) + " " + entity_value
                else:
                    composed_entity = None
            elif re.match(r"B-(.*)", entity_name):
                self.begin_entity = True
                composed_entity = entity
                composed_entity["entity"] = composed_entity["entity"][2:]
            elif self.begin_entity and composed_entity is not None:
                composed_entities.append(composed_entity)
                self.begin_entity = False
                composed_entity = None

        if self.begin_entity and composed_entity is not None:
            composed_entities.append(composed_entity)

        return composed_entities