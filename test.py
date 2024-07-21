import os
from groq import Groq
from config import groq_api
client = Groq(api_key=groq_api)
filename = 'output.wav'

with open(filename, "rb") as file:
    print('cow1')
    transcription = client.audio.transcriptions.create(
      file=(filename, file.read()),
      model="whisper-large-v3",
      # prompt="Specify context or spelling",  # Optional
      response_format="json",  # Optional
      language="en",  # Optional
      
    )
    print(transcription.text)