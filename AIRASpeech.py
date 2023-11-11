from typing import Any
from transformers import AutoProcessor, AutoModel
import scipy
import torch
import pygame

class BarkSpeech():

    def __init__(self):
        self.processor = AutoProcessor.from_pretrained("suno/bark-small")
        self.model = AutoModel.from_pretrained("suno/bark-small")        
        self.model = self.model.cuda()
        self.model =  self.model.to_bettertransformer()
        # self.model = self.model.to_bettertransformers()

        pygame.init()

    def __call__(self, text):

        voice_preset = "v2/en_speaker_6"

        inputs = self.processor(
            text=[text],
            return_tensors="pt",
            voice_preset=voice_preset
        )

        inputs['input_ids'] = inputs['input_ids'].cuda()
        inputs['attention_mask'] = inputs['attention_mask'].cuda()
        inputs['history_prompt']['semantic_prompt'] = inputs['history_prompt']['semantic_prompt'].cuda()
        inputs['history_prompt']['coarse_prompt'] = inputs['history_prompt']['coarse_prompt'].cuda()
        inputs['history_prompt']['fine_prompt'] = inputs['history_prompt']['fine_prompt'].cuda()
        with torch.inference_mode():

            speech_values = self.model.generate(**inputs, do_sample=True)
            sampling_rate = self.model.generation_config.sample_rate
            scipy.io.wavfile.write("bark_out.wav", rate=sampling_rate, data=speech_values.cpu().numpy().squeeze())

        pygame.mixer.music.load('bark_out.wav')
        pygame.mixer.music.play()
        audio_duration = pygame.mixer.Sound('bark_out.wav').get_length() * 1000
        pygame.time.wait(int(audio_duration))

if __name__ == "__main__":
    B = BarkSpeech()
    B("""AIRA: [laughs] Yo, let me drop a rhyme about Kollada, the word that's got universal power, nada.
When you don't know what to say, just use it, and it'll be your verbal DJ.""")


        
