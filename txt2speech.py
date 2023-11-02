from numpy import frombuffer, int16
from pyaudio import PyAudio,paInt16
import whisper
import audioop  

class STT:
    def __init__(self, model_name='small.en', max_silence_seconds=2, silence_threshold=2000, chunk=1024, sample_format=paInt16, channels=1, fs=16000, max_seconds=60):
        print('Loading model')
        self.model = whisper.load_model(model_name)
        self.chunk = chunk 
        self.sample_format = sample_format
        self.channels = channels
        self.fs = fs
        self.max_seconds = max_seconds
        self.silence_threshold = silence_threshold
        self.max_silence_seconds = max_silence_seconds
        self.p = PyAudio()
        # self.stream = self.p.open(format=self.sample_format,
        #             channels=self.channels,
        #             rate=self.fs,
        #             frames_per_buffer=self.chunk,
        #             input=True)
        self.stream = None
    def listen(self):
        '''
        If it is all zeros, it means that you have to calibrate the silence_threshold to a higher value.
        '''

        frames = []
        self.p = PyAudio()
        self.stream = self.p.open(format=self.sample_format,
                    channels=self.channels,
                    rate=self.fs,
                    frames_per_buffer=self.chunk,
                    input=True)

        print("Recording...")
        ct = 0
        while True:
            data = self.stream.read(self.chunk)
            frames.append(data)
            rms = audioop.rms(data, 2)

            if rms < self.silence_threshold:
                ct += 1
            else:
                ct = 0
            # print(ct)
            if ct == 16*self.max_silence_seconds:
                break

            if len(frames) * self.chunk / self.fs > self.max_seconds:
                break

        self.stream.stop_stream()
        self.stream.close()
        print("Recording completed.")
        return frames


    def transcribe(self, frames):
        audio_data = frombuffer(b''.join(frames), dtype=int16)
        audio_data = audio_data.astype('float32') / 32767.0
        result = self.model.transcribe(audio_data)
        self.p.terminate()
        return result["text"]

class TTS:
    def speak(self, text,rate=170, volume=0.75):
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', rate) 
        engine.setProperty('volume', volume) 
        engine.say(text)
        engine.runAndWait()
        engine.stop()


if __name__ == '__main__':
    
    obj = STT()

    while True:

        voice = obj.listen()
        ans = obj.transcribe(voice)
        print(ans)

    # obj = TTS()
    # obj.speak(ans)

