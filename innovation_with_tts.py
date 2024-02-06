'''
If listen mode listen_mode out zeros, you need to adjust(lower) the silence threshold '''

from numpy import frombuffer, int16
from pyaudio import PyAudio,paInt16
import whisper
import audioop  

# Parameters to calibrate
silence_thresh = 700 # Adjusts the volume level to be considered 'silent'.
max_duration = 60 # Max recording duration, regardless of everything else.
max_silence_seconds = 2 # How much silence duration is to be considered 'done talking'
model_name = 'small.en' # Whisper model

debug_mode = False # Shows the voice threshold. Should be higher than silence threshold to detect

listen_mode = True # Shows if AIRA is detecting the voice

class STT:
    def __init__(self, model_name=model_name, max_silence_seconds=max_silence_seconds, 
                 silence_threshold=silence_thresh, chunk=1024, 
                 sample_format=paInt16, channels=1, fs=16000, 
                 max_seconds=max_duration):
        if debug_mode:
            print('Initalizing Ears')
        self.model = whisper.load_model(model_name)
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
        #If it is all zeros, it means that you have to calibrate the silence_threshold to a higher value.
    
        frames = []
        self.p = PyAudio()
        self.stream = self.p.open(format=self.sample_format,
                    channels=self.channels,
                    rate=self.fs,
                    frames_per_buffer=self.chunk,
                    input=True)

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
                print(f'Threshold: {rms}')
            if listen_mode:
                print(f'Hearing: {ct}')

            if ct == 16*self.max_silence_seconds:
                break
            # if len(frames) * self.chunk / self.fs > self.max_seconds:
            #     break
            
        above_threshold_detected = False
        
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
    def speak(self, text,rate=170, volume=1):
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
        try:
            voice = obj.listen()
            ans = obj.transcribe(voice)
            print(ans)
        except KeyboardInterrupt:
            break

