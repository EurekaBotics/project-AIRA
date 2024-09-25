"""
If listen mode listen_mode out zeros, you need to adjust(lower) the silence threshold """

from numpy import frombuffer, int16
from pyaudio import PyAudio, paInt16
import whisper
import audioop
import wave
from groq import Groq
import os
from queue import Queue
import speech_recognition as sr
from sys import platform
from time import sleep
from datetime import datetime, timedelta

groq_api = os.environ.get("GROQ_API_KEY")

# Parameters to calibrate
silence_thresh = 1000  # Adjusts the volume level to be considered 'silent'.
max_duration = 60  # Max recording duration, regardless of everything else.
max_silence_seconds = 2  # How much silence duration is to be considered 'done talking'
model_name = "small.en"  # Whisper model

debug_mode = (
    True  # Shows the voice threshold. Should be higher than silence threshold to detect
)

listen_mode = True  # Shows if AIRA is detecting the voice


class STT:
    def __init__(
        self,
        model_name=model_name,
        max_silence_seconds=max_silence_seconds,
        silence_threshold=silence_thresh,
        chunk=1024,
        sample_format=paInt16,
        channels=1,
        fs=16000,
        max_seconds=max_duration,
    ):
        if debug_mode:
            print("Initalizing Ears")
        # self.model = whisper.load_model(model_name)
        self.client = Groq(api_key=groq_api)
        self.chunk = chunk
        self.sample_format = sample_format
        self.channels = channels
        self.fs = fs
        self.max_seconds = max_seconds
        self.silence_threshold = silence_threshold
        self.max_silence_seconds = max_silence_seconds
        self.p = PyAudio()
        self.stream = None

    def listen(self):
        # If it is all zeros, it means that you have to calibrate the silence_threshold to a higher value.

        frames = []
        self.p = PyAudio()
        self.stream = self.p.open(
            format=self.sample_format,
            channels=self.channels,
            rate=self.fs,
            frames_per_buffer=self.chunk,
            input=True,
        )

        print("Listening...")
        ct = 0
        above_threshold_detected = False
        while True:
            data = self.stream.read(self.chunk)
            frames.append(data)
            rms = audioop.rms(data, 2)
            if not above_threshold_detected and rms < silence_thresh:
                frames.pop()

            if rms > silence_thresh:
                above_threshold_detected = True
                # print('Big boy')

            if above_threshold_detected:
                if rms < self.silence_threshold:
                    ct += 1
                else:
                    ct = 0

            if debug_mode:
                print(f"Threshold: {rms}")
            if listen_mode:
                print(f"Hearing: {ct}")

            if ct == 16 * self.max_silence_seconds:
                break
            # if len(frames) * self.chunk / self.fs > self.max_seconds:
            #     break

        above_threshold_detected = False

        self.stream.stop_stream()
        self.stream.close()
        print("Recording completed.")
        return frames

    def transcribe(self, frames):
        # audio_data = frombuffer(b"".join(frames), dtype=int16)
        # audio_data = audio_data.astype("float32") / 32767.0
        # result = self.model.transcribe(audio_data)
        # self.p.terminate()
        cache_file = "output.wav"
        wf = wave.open(cache_file, "wb")
        wf.setnchannels(1)

        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(b"".join(frames))
        wf.close()

        with open(cache_file, "rb") as file:
            transcription = self.client.audio.transcriptions.create(
                file=(cache_file, file.read()),
                model="whisper-large-v3",
                # prompt="Specify context or spelling",  # Optional
                response_format="json",  # Optional
                language="en",  # Optional
            )

        return transcription.text


class TTS:
    def speak(self, text, rate=170, volume=1):
        import pyttsx3

        engine = pyttsx3.init()
        engine.setProperty("rate", rate)
        engine.setProperty("volume", volume)
        engine.say(text)
        engine.runAndWait()
        engine.stop()


class RealTimeTranscription:
    def __init__(
        self,
        cache_file="temp_audio.wav",
        energy_threshold=1000,
        record_timeout=2.0,
        phrase_timeout=3.0,
        default_microphone="pulse",
    ):
        groq_api = os.environ.get("GROQ_API_KEY")
        self.client = Groq(api_key=groq_api)
        self.cache_file = cache_file
        self.energy_threshold = energy_threshold
        self.record_timeout = record_timeout
        self.phrase_timeout = phrase_timeout
        self.default_microphone = default_microphone
        self.data_queue = Queue()
        self.transcription = [""]
        self.phrase_time = None

        self.recorder = sr.Recognizer()
        self.recorder.energy_threshold = self.energy_threshold
        self.recorder.dynamic_energy_threshold = True

        self.source = self._get_microphone_source()

    def _get_microphone_source(self):
        if "linux" in platform:
            mic_name = self.default_microphone
            if not mic_name or mic_name == "list":
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
            print(f'Microphone with name "{name}" found')

    def _record_callback(self, _, audio: sr.AudioData):
        self.data_queue.put(audio.get_wav_data())

    def start_listening(self):
        with self.source:
            self.recorder.adjust_for_ambient_noise(self.source)
        self.recorder.listen_in_background(
            self.source, self._record_callback, phrase_time_limit=self.record_timeout
        )
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

        audio_data = b"".join(self.data_queue.queue)
        self.data_queue.queue.clear()

        self._save_audio_cache(audio_data)
        transcription = self._transcribe_audio()

        if phrase_complete:
            self.transcription.append(transcription)
        else:
            if self.transcription:
                self.transcription[-1] = f"{self.transcription[-1]} {transcription}"

        self._clear_console()
        print("\n".join(self.transcription), end="", flush=True, color="green")

    def _save_audio_cache(self, audio_data):
        with open(self.cache_file, "wb") as f:
            f.write(audio_data)

    def _clear_console(self):
        os.system("cls" if os.name == "nt" else "clear")

    def _graceful_exit(self):
        print("\nShutting down gracefully...")
        self._print_transcription()
        exit()

    def _check_phrase_complete(self, now):
        return self.phrase_time and now - self.phrase_time > timedelta(
            seconds=self.phrase_timeout
        )

    def _transcribe_audio(self):
        valid_extensions = (
            ".wav",
            ".flac",
            ".mp3",
            ".mp4",
            ".mpeg",
            ".mpga",
            ".m4a",
            ".ogg",
            ".opus",
            ".webm",
        )

        if not self.cache_file.endswith(valid_extensions):
            raise ValueError(
                f"Unsupported file format for transcription. Supported formats are: {valid_extensions}"
            )

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


# devanand

if __name__ == "__main__":

    obj = STT()
    while True:
        try:
            voice = obj.listen()
            ans = obj.transcribe(voice)
            print(ans)
        except KeyboardInterrupt:
            break
