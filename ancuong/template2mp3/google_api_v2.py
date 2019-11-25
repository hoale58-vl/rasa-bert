from google.cloud import texttospeech

import html

def ssml_to_audio(ssml_text, outfile):
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

    with open(outfile, 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file ' + outfile)

def text_to_ssml(raw_lines):

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

def main():
    plaintext = 'Việt Hòa đẹp trai quá, tài giỏi nữa. Yêu Việt Hòa quá đi! Việt Hòa đang ở đâu vậy?'
    ssml_text = text_to_ssml(plaintext)
    ssml_to_audio(ssml_text, 'example.mp3')


if __name__ == '__main__':
    main()