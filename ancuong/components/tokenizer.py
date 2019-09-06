import re
from typing import Any, List, Text

from rasa.nlu.components import Component
from rasa.nlu.config import RasaNLUModelConfig
from rasa.nlu.tokenizers import Token, Tokenizer
from rasa.nlu.training_data import Message, TrainingData
from CocCocTokenizer import PyTokenizer

class MyTokenizer(Tokenizer, Component):
    provides = ["tokens"]
    requires = ["lang"]

    def __init__(self, component_config=None):
        super(MyTokenizer, self).__init__(component_config)
        self.T = PyTokenizer(load_nontone_data=True)

    def train(
        self, training_data: TrainingData, config: RasaNLUModelConfig, **kwargs: Any
    ) -> None:
        for example in training_data.training_examples:
            lang = example.get("lang", None)
            if lang is not None:
                example.set("tokens", self.tokenize(example.text, lang))
            else:
                example.set("tokens", [])

    def process(self, message: Message, **kwargs: Any) -> None:
        text = message.text
        lang = message.get("lang", None)
        if lang is not None:
            message.set("tokens", self.tokenize(text, lang))
        else:
            message.set("tokens", [])

    def tokenize(self, text: Text, lang) -> List[Token]:
        text = text.lower()

        if lang in ['vi']:
            text = re.sub(r"(mày|cậu|mi|ngươi|mầy)", "bạn", text)
            text = re.sub(r"(tao|tớ|mình|tui)", "tôi", text)
            words = self.T.word_tokenize(text, tokenize_option=0)
        else:
            words = text.split()

        running_offset = 0
        tokens = []
        text = text.replace(" ", "_")

        for word in words:
            word_offset = text.index(word, running_offset)
            word_len = len(word)
            running_offset = word_offset + word_len
            tokens.append(Token(word, word_offset))
        return tokens