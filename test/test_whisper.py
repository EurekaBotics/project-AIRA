import argparse
import os
import speech_recognition as sr
from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform
from groq import Groq
from print_color import print

class RealTimeTranscription:
    def __init__(self, cache_file="temp_audio.wav", energy_threshold=1000, 
                 record_timeout=2.0, phrase_timeout=3.0, default_microphone="pulse"):
        groq_api = os.environ.get("GROQ_API_KEY")
        self.client = Groq(api_key=groq_api) 
        self.cache_file = cache_file  
        self.energy_threshold = energy_threshold
        self.record_timeout = record_timeout
        self.phrase_timeout = phrase_timeout
        self.default_microphone = default_microphone
        self.data_queue = Queue()
        self.transcription = ['']
        self.phrase_time = None

        self.recorder = sr.Recognizer()
        self.recorder.energy_threshold = self.energy_threshold
        self.recorder.dynamic_energy_threshold = True

        self.source = self._get_microphone_source()

    def _get_microphone_source(self):
        if 'linux' in platform:
            mic_name = self.default_microphone
            if not mic_name or mic_name == 'list':
                self._list_microphones()
                exit()
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                if mic_name in name:
                    return sr.Microphone(sample_rate=16000, device_index=index)
        else:
            return sr.Microphone(sample_rate=16000)

    @staticmethod
    def _list_microphones():
        print("Available microphone devices:")
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"Microphone with name \"{name}\" found")

    def _record_callback(self, _, audio: sr.AudioData):
        self.data_queue.put(audio.get_wav_data())

    def start_listening(self):
        with self.source:
            self.recorder.adjust_for_ambient_noise(self.source)
        self.recorder.listen_in_background(self.source, self._record_callback, phrase_time_limit=self.record_timeout)
        print("Listening...\n")
        self._process_audio()

    def _process_audio(self):
        try:
            while True:
                if not self.data_queue.empty():
                    self._handle_transcription()
                else:
                    sleep(0.1)
        except KeyboardInterrupt:
            self._graceful_exit()

    def _handle_transcription(self):
        now = datetime.utcnow()
        phrase_complete = self._check_phrase_complete(now)
        self.phrase_time = now

        audio_data = b''.join(self.data_queue.queue)
        self.data_queue.queue.clear()

        self._save_audio_cache(audio_data)
        transcription = self._transcribe_audio()

        if phrase_complete:
            self.transcription.append(transcription)
        else:
            if self.transcription:
               self.transcription[-1] = f"{self.transcription[-1]} {transcription}"

        self._clear_console()
        print("\n".join(self.transcription), end='', flush=True, color='green')

    def _save_audio_cache(self, audio_data):
        with open(self.cache_file, "wb") as f:
            f.write(audio_data)

    def _clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _graceful_exit(self):
        print("\nShutting down gracefully...")
        self._print_transcription()
        exit()

    def _check_phrase_complete(self, now):
        return self.phrase_time and now - self.phrase_time > timedelta(seconds=self.phrase_timeout)

    def _transcribe_audio(self):
        valid_extensions = ('.wav', '.flac', '.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.ogg', '.opus', '.webm')
        
        if not self.cache_file.endswith(valid_extensions):
            raise ValueError(f"Unsupported file format for transcription. Supported formats are: {valid_extensions}")

        try:
            with open(self.cache_file, "rb") as file:
                file_content = file.read()
                if not file_content:
                    raise ValueError("The audio file is empty or could not be read.")
                
                transcription = self.client.audio.transcriptions.create(
                    file=(self.cache_file, file_content),
                    model="whisper-large-v3",
                    response_format="json",
                    language="en",
                )
            return transcription.text
        except Exception as e:
            print(f"An error occurred during transcription: {e}")
            return ""

    def _print_transcription(self):
        print("\n\nFinal Transcription:")
        print("\n".join(self.transcription))
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache_file", default="temp_audio.wav", help="Temporary audio file name")
    parser.add_argument("--energy_threshold", default=500, type=int)
    parser.add_argument("--record_timeout", default=2.0, type=float)
    parser.add_argument("--phrase_timeout", default=3.0, type=float)
    parser.add_argument("--default_microphone", default='pulse' if 'linux' in platform else None, type=str)

    args = parser.parse_args()

    transcription = RealTimeTranscription(cache_file=args.cache_file,
                                          energy_threshold=args.energy_threshold, 
                                          record_timeout=args.record_timeout,
                                          phrase_timeout=args.phrase_timeout,
                                          default_microphone=args.default_microphone)
    transcription.start_listening()