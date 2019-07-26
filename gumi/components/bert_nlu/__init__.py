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
from pytorch_pretrained_bert import BertModel, BertTokenizer
import itertools
import numpy as np

emb_size = None
hidden_size = 200 # 100, 200 
bidirectional = True
num_layers = 1
dropout = 0.1 # 0.1, 0.5 
fix_bert_model = None
multiClass = False
encoder_info_filter = lambda info: info



class BertNLU(Component):
    name = "bert_nlu"
    provides = ["intent", "entities"]
    provides = []
    requires = ["tokens"]
    defaults = {}
    language_list = ["en", "vi", "jp"]

    def __init__(self, component_config=None):
        super(BertNLU, self).__init__(component_config)
        self.model_dir = os.path.join(os.path.dirname(__file__), "model")
        self.tag_to_idx, self.idx_to_tag = vocab_reader.read_vocab_file(os.path.join(self.model_dir,'vocab.tag'), bos_eos=False, no_pad=True, no_unk=True)
        self.class_to_idx, self.idx_to_class = vocab_reader.read_vocab_file(os.path.join(self.model_dir,'vocab.class'), bos_eos=False, no_pad=True, no_unk=True)
        self.device = torch.device("cpu")
        self.load_model()

    def load_model(self):
        bert_model_name = "bert-base-uncased"
        self.tokenizer = BertTokenizer.from_pretrained(bert_model_name)
        self.model_bert = BertModel.from_pretrained(bert_model_name)
        self.model_tag = slot_tagger.LSTMTagger(emb_size, hidden_size, None, len(self.tag_to_idx), 
                                       bidirectional=bidirectional, 
                                       num_layers=num_layers, 
                                       dropout=dropout, 
                                       device=self.device, 
                                       bert_model=self.model_bert, 
                                       fix_bert_model=fix_bert_model)

        self.model_class = snt_classifier.sntClassifier_hiddenAttention(hidden_size, len(self.class_to_idx), 
                                                               bidirectional=bidirectional, 
                                                               num_layers=num_layers, 
                                                               dropout=dropout, 
                                                               device=self.device, 
                                                               multi_class=multiClass)
        
        self.model_tag.load_model(os.path.join(self.model_dir,'model.tag'))
        self.model_class.load_model(os.path.join(self.model_dir,'model.class'))

        self.model_tag = self.model_tag.to(self.device)
        self.model_class = self.model_class.to(self.device)

        self.model_tag.eval()
        self.model_class.eval()

    def prepare_inputs_for_bert(self, sentences, word_lengths):
        ## sentences are sorted by sentence length
        max_length_of_sentences = max(word_lengths)
        tokens = []
        selected_indexes = []
        start_pos = 0
        for ws in sentences:
            selected_index = []
            ts = self.tokenizer.tokenize('[CLS]')
            for w in ws:
                selected_index.append(len(ts))
                ts += self.tokenizer.tokenize(w)
            ts += self.tokenizer.tokenize('[SEP]')
            tokens.append(ts)
            selected_indexes.append(selected_index)
        max_length_of_tokens = max([len(tokenized_text) for tokenized_text in tokens])
        assert max_length_of_tokens <= self.model_bert.config.max_position_embeddings
        input_mask = [[1] * len(tokenized_text) + [0] * (max_length_of_tokens - len(tokenized_text)) for tokenized_text in tokens]
        indexed_tokens = [self.tokenizer.convert_tokens_to_ids(tokenized_text + ['[PAD]'] * (max_length_of_tokens - len(tokenized_text))) for tokenized_text in tokens]
        segments_ids = [[0] * max_length_of_tokens for tokenized_text in tokens]
        selected_indexes = [[idx + i * max_length_of_tokens for idx in selected_index] for i, selected_index in enumerate(selected_indexes)]
        copied_indexes = [[idx + i * max_length_of_sentences for idx in range(length)] for i, length in enumerate(word_lengths)]

        input_mask = torch.tensor(input_mask, dtype=torch.long, device=self.device)
        tokens_tensor = torch.tensor(indexed_tokens, dtype=torch.long, device=self.device)
        segments_tensor = torch.tensor(segments_ids, dtype=torch.long, device=self.device)
        selects_tensor = torch.tensor(list(itertools.chain.from_iterable(selected_indexes)), dtype=torch.long, device=self.device)
        copies_tensor = torch.tensor(list(itertools.chain.from_iterable(copied_indexes)), dtype=torch.long, device=self.device)
        return {'tokens': tokens_tensor, 'segments': segments_tensor, 'selects': selects_tensor, 'copies': copies_tensor, 'mask': input_mask}


    def train(self, training_data, cfg, **kwargs):
        """Train this component.

        This is the components chance to train itself provided
        with the training data. The component can rely on
        any context attribute to be present, that gets created
        by a call to :meth:`components.Component.pipeline_init`
        of ANY component and
        on any context attributes created by a call to
        :meth:`components.Component.train`
        of components previous to this one."""
        pass

    def process(self, message, **kwargs):
        """Retrieve the tokens of the new message, pass it to the classifier
            and append prediction results to the message class."""

        tokens = [t.text for t in message.get("tokens")]
        inputs = self.prepare_inputs_for_bert([tokens], [len(tokens)])

        tag_scores, encoder_info = self.model_tag(inputs, [len(tokens)], with_snt_classifier=True)
        top_pred_slots = tag_scores.data.cpu().numpy().argmax(axis=-1)


        entities = []
        pre_entity = "O"
        entity_value = ""
        for idx, slot in enumerate(top_pred_slots[0]):
            entity = list(self.tag_to_idx.keys())[list(self.tag_to_idx.values()).index(slot)]
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
        message.set("entities", entities, add_to_output=True)

        class_scores = self.model_class(encoder_info_filter(encoder_info))
        snt_probs = class_scores.data.cpu().numpy()

        intent = {"name": self.idx_to_class[snt_probs.argmax(axis=-1)[0]], "confidence": float(np.exp(snt_probs.max(axis=-1))[0])}
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