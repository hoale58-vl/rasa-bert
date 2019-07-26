import re
from typing import Any

from rasa.nlu.components import Component
from rasa.nlu.training_data import Message
from langdetect import detect_langs

class LangDetect(Component):
    provides = ["lang"]

    def process(self, message: Message, **kwargs: Any) -> None:
        message.set("lang", detect_langs(message.text)[0].lang, add_to_output=True)
        