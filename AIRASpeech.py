from transformers import AutoProcessor, AutoModel
import scipy
import time

processor = AutoProcessor.from_pretrained("suno/bark-small")
model = AutoModel.from_pretrained("suno/bark-small")

model = model.cuda()
# AIRA: Hi I am AIRA, An Intelligent Robot Assistant. I am so happy to be here. [laughs] My name is an acronym Actually, It goes like this An Intelligent Robot Assistant.
inputs = processor(
    text=["AIRA: Hi I am AIRA, An Intelligent Robot Assistant. I am so happy to be here. [laughs] My name is an acronym Actually, It goes like this An Intelligent Robot Assistant."],
    return_tensors="pt",
)

inputs['input_ids'] = inputs['input_ids'].cuda()
inputs['attention_mask'] = inputs['attention_mask'].cuda()

start_time = time.time() # record the start time
speech_values = model.generate(**inputs, do_sample=True)
end_time = time.time() # record the end time
execution_time = end_time - start_time # calculate the execution time
print(f"Execution time: {execution_time} seconds") # print the execution time
print("Got here")
sampling_rate = model.generation_config.sample_rate
scipy.io.wavfile.write("bark_out.mp3", rate=sampling_rate, data=speech_values.cpu().numpy().squeeze())
