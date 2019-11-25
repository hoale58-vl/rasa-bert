#!/usr/bin/python
# -*- coding: utf8 -*-
from google.cloud import texttospeech

import html

import os

output_dir = "./output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

class Text2Speed:
    def ssml_to_audio(self, name, ssml_text):
        client = texttospeech.TextToSpeechClient.from_service_account_json("cre.json")
        synthesis_input = texttospeech.types.SynthesisInput(ssml=ssml_text)

        # Builds the voice request, selects the language code ("en-US") and
        # the SSML voice gender ("MALE")
        voice = texttospeech.types.VoiceSelectionParams(
            language_code='vi-VN',
            name='vi-VN-Wavenet-A',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3,
            speaking_rate=0.85,
            pitch=4.8,
            volume_gain_db=3.0
            )

        response = client.synthesize_speech(synthesis_input, voice, audio_config)

        with open(os.path.join(output_dir, name + '.mp3'), 'wb') as out:
            out.write(response.audio_content)

    def text_to_ssml(self, raw_lines):

        escaped_lines = html.escape(raw_lines)
        escaped_lines = escaped_lines.replace('.', '.<break time="1s"/>')
        escaped_lines = escaped_lines.replace(',', ',<break time="0.5s"/>')
        escaped_lines = escaped_lines.replace('?', '?<break time="1s"/>')
        escaped_lines = escaped_lines.replace('!', '!<break time="1s"/>')
        # Convert plaintext to SSML
        # Wait two seconds between each address
        ssml = '<speak>{}</speak>'.format(
            escaped_lines.replace('\n', '\n<break time="2s"/>'))

        return ssml
