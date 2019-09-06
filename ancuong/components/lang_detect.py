import re
from typing import Any

from rasa.nlu.components import Component
# from langdetect import detect_langs
import langid
from rasa.nlu.training_data import Message, TrainingData
from rasa.nlu.config import RasaNLUModelConfig
langid.set_languages(['en', 'vi'])

class LangDetect(Component):
    provides = ["lang"]

    def train(
        self, training_data: TrainingData, config: RasaNLUModelConfig, **kwargs: Any
    ) -> None:
        for example in training_data.training_examples:
            lang, score = langid.classify(example.text)
            example.set("lang", lang, add_to_output=True)
            # example.set("lang", detect_langs(example.text)[0].lang, add_to_output=True)

    def process(self, message: Message, **kwargs: Any) -> None:
        lang, score = langid.classify(message.text)
        message.set("lang", lang, add_to_output=True)

        # Add lang to slot for domain - utter
        entities = []
        entities.append({
                "value" : lang,
                "entity" : "lang"
            })
        message.set("entities", message.get("entities", []) + entities)
        # message.set("lang", detect_langs(message.text)[0].lang, add_to_output=True)
        
        