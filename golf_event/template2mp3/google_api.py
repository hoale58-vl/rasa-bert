#!/usr/bin/python
# -*- coding: utf8 -*-
from google.cloud import texttospeech_v1beta1
import os

output_dir = "./output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

class Text2Speed:
    def downloadFile(self,name, text):
        client = texttospeech_v1beta1.TextToSpeechClient.from_service_account_json("cre.json")
        audioConfig = {
            "audio_encoding": "MP3",
            "pitch": 4.8,
            "speaking_rate": 1.10,
            "volume_gain_db": 3.0
        }
        input_ = {
            "text": text
        }
        voice = {
            "language_code": "vi-VN",
            "name": "vi-VN-Wavenet-A"
        }
        response = client.synthesize_speech(input_, voice, audioConfig)
        with open(os.path.join(output_dir, name + '.mp3'), 'wb') as out:
            out.write(response.audio_content)