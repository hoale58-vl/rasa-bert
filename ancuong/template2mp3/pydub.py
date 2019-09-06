from pydub import AudioSegment

song = AudioSegment.from_mp3("music.mp3")
utter = AudioSegment.from_mp3("utter_ask_show_room_vi_0.mp3")

music_start = 12.7 * 1000

first_12_seconds_frame = utter[:music_start]
remain_seconds_frame = utter[music_start:]

second_of_silence = 2 * 1000
silence_frame = AudioSegment.silent(duration=second_of_silence)
concatenate = silence_frame + remain_seconds_frame

overlay = concatenate.overlay(song)
second_of_silence = 1 * 1000
silence_frame = AudioSegment.silent(duration=second_of_silence)
concatenate = first_12_seconds_frame + silence_frame + overlay

concatenate.export("mix.mp3", format="mp3")
