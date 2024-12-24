import os
from typing import Optional
import tempfile
import wave
import pyaudio
import speech_recognition as sr
from gtts import gTTS
from pyttsx3 import init as pyttsx3_init
import numpy as np


class AudioUtils:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.offline_engine = pyttsx3_init()
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100

    def text_to_speech_online(
        self, text: str, output_file: Optional[str] = None, lang: str = "en"
    ) -> Optional[str]:
        try:
            tts = gTTS(text=text, lang=lang)

            if output_file is None:
                temp_dir = tempfile.gettempdir()
                output_file = os.path.join(temp_dir, "tts_output.mp3")

            tts.save(output_file)
            return output_file

        except Exception as e:
            print(f"Error in text_to_speech_online: {str(e)}")
            return None

    def text_to_speech_offline(
        self, text: str, rate: int = 150, volume: float = 1.0
    ) -> None:
        try:
            self.offline_engine.setProperty("rate", rate)
            self.offline_engine.setProperty("volume", volume)
            self.offline_engine.say(text)
            self.offline_engine.runAndWait()

        except Exception as e:
            print(f"Error in text_to_speech_offline: {str(e)}")

    def record_audio(self, output_file: str, duration: int = 5) -> Optional[str]:
        try:
            p = pyaudio.PyAudio()

            stream = p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
            )

            print(f"Recording for {duration} seconds...")
            frames = []

            for _ in range(0, int(self.RATE / self.CHUNK * duration)):
                data = stream.read(self.CHUNK)
                frames.append(data)

            print("Recording finished")

            stream.stop_stream()
            stream.close()
            p.terminate()

            with wave.open(output_file, "wb") as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(p.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b"".join(frames))

            return output_file

        except Exception as e:
            print(f"Error in record_audio: {str(e)}")
            return None

    def speech_to_text_from_mic(self, duration: int = 5) -> Optional[str]:
        try:
            with sr.Microphone() as source:
                print("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source)

                print(f"Listening for {duration} seconds...")
                audio = self.recognizer.listen(source, timeout=duration)

            text = self.recognizer.recognize_google(audio)
            return text

        except Exception as e:
            print(f"Error in speech_to_text_from_mic: {str(e)}")
            return None


def demo_tts(text: str = "Hello, this is a test of text to speech conversion"):
    audio_utils = AudioUtils()

    print("Testing online TTS...")
    output_file = audio_utils.text_to_speech_online(text)
    if output_file:
        print(f"Audio saved to: {output_file}")

    print("\nTesting offline TTS...")
    audio_utils.text_to_speech_offline(text)


def demo_stt(duration: int = 5):
    audio_utils = AudioUtils()

    print("\nTesting direct microphone STT...")
    text = audio_utils.speech_to_text_from_mic(duration)
    if text:
        print(f"Transcribed text: {text}")

    print("\nTesting recorded audio STT...")
    recorded_file = "recorded_audio.wav"
    if audio_utils.record_audio(recorded_file, duration):
        text = audio_utils.speech_to_text_from_file(recorded_file)
        if text:
            print(f"Transcribed text: {text}")
        os.remove(recorded_file)


if __name__ == "__main__":
    demo_tts()
    demo_stt()
