import struct
import pyaudio
import pvporcupine
from txt2speech import STT 

porcupine = None
paud = None
audio_stream = None
stt = STT()

try:
    access_key = "u31o87yvNPqHJJZUEDUTWxG16ERWFT4pqE2CNcSz8Jo1XH818WDzrg==" 
    porcupine = pvporcupine.create(access_key=access_key,
                                    keyword_paths=['wake-word-windows.ppn'],

                                    keywords=['hey chappy'])
    paud = pyaudio.PyAudio()
    audio_stream = paud.open(rate=porcupine.sample_rate,
                             channels=1,
                             format=pyaudio.paInt16,
                             input=True,
                             frames_per_buffer=porcupine.frame_length)
    
    while True:
        keyword = audio_stream.read(porcupine.frame_length)
        keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
        keyword_index = porcupine.process(keyword)
        if keyword_index >= 0:
            print("Hotword detected")
            print(keyword)
            # voice = stt.listen()
            # msg = stt.transcribe(voice)

finally:
    if porcupine is not None:
        porcupine.delete()
    if audio_stream is not None:
        audio_stream.close()
    if paud is not None:
        paud.terminate()