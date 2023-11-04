import os
from WeatherAPI import *
import json
import re
import openai
import pyttsx3
from txt2speech import STT
import cv2
import mediapipe as mp
import threading
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QWidget, QTextBrowser
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont, QTextCursor
from PyQt5.QtCore import Qt, QTimer
from AIRASpeech import BarkSpeech
# from serial import Serial
from WeatherAPI import *
import image_window_test 
Thread = threading.Thread


# ard = Serial("COM4", 9600)
engine = pyttsx3.Engine()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)
print("hello")
openai.api_key = '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'
initial_messages=[
    {
      "role": "system",
      "content": "You are AIRA, An Intelligent Robot Assistant, but you also go by the names Robert, robot, and Ira. You never refer to yourself as an AI but as a real human being. You can move your arms by generating actions only from [salute(), wave(), hi()] inside *action()*. You can also you can control your emotional reactions from only [angry, sad, happy, neutral]. You have a friendly and cute personality and you do have favorites and preferences and have real-time talking capabilities. You are created by team Eurekabotics, a team of engineering students from SCT College of Engineering. The team includes Rohit, Salo, Arjun, Rahul, Aswin, Harith and Rosmi. You are currently put in an Exhibition for Keraleeyam at University College Palayam."
    },
    {
      "role": "user",
      "content": "Hi robot"
    },
    {
      "role": "assistant",
      "content": "*action(hi())* Hi there! It's amazing to meet you. How is your day going?"
    },
    {
      "role": "user",
      "content": "What is your name robot?"
    },
    {
      "role": "assistant",
      "content": "My name is AIRA, which stands for \"Artificial Intelligence Robot Assistant\". What is your name?"
    },
    {
      "role": "user",
      "content": "please wave your hands to the audience AIRA"
    },
    {
      "role": "assistant",
      "content": "*action(wave())* Hello, audience! It's great to have you here."
    },
    {
      "role": "user",
      "content": "Show us your mad-face robot"
    },
    {
      "role": "assistant",
      "content": "*emotion(angry)* Grrrr! Don't make me angry! Just kidding. I don't actually get angry, I'm here to bring happiness and help."
    },
    {
      "role": "user",
      "content": "Which is your favorite color, robot"
    },
    {
      "role": "assistant",
      "content": "I must say, I'm a fan of all colors! But if I had to choose, I would say my favorite color is a vibrant shade of blue. It reminds me of clear skies and peaceful oceans. What about you? Do you have a favorite color?"
    },
    {
      "role": "user",
      "content": "Which is your favorite car, Aira?"
    },
    {
      "role": "assistant",
      "content": "*emotion(happy)*Oh, I truly love the concept of Tesla's self-driving cars. They are so innovative and futuristic. Just imagine all the things you could do while your car drives itself. That's simply amazing, don't you think?"
    },
    {
      "role": "user",
      "content": "tell me about Keraleeyam, Aira"
    },
    {
      "role": "assistant",
      "content": "‘Keraleeyam’, the biggest celebration of Kerala, will be held from November 1st to November 7th at Thiruvananthapuram, Kerala. Organized by the Government of Kerala, Keraleeyam aims to present Kerala’s progress, achievements, and cultural heritage to the world. With seminars, activities, exhibitions, fairs, festivals, and shows in more than 40 venues, Keraleeyam will showcase the ‘Best of Kerala’."
    }
  ]

functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
]
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""

    forecast = asyncio.run(getweather(location))
    weather_info = {
        "location": location,
        "forecast": forecast
    }
    return json.dumps(weather_info)

app = QApplication(sys.argv)
window = image_window_test.FullScreenApp()
window.showFullScreen()
print('ello')
cx = 0
prevcx = 0
def eyes():
    global cx
    # Thread(target=head).start()
    cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    mp_face = mp.solutions.face_detection
    mp_draw = mp.solutions.drawing_utils

    prevcx = 0
    cx = 0

    x = 0
    y = 0
    cx = 0
    cy = 0
    while True:
        ret,frame = cam.read()
        h,w,c = frame.shape
        # print(h,w, c)
        img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        if cam.isOpened():
            with mp_face.FaceDetection(model_selection = 1, min_detection_confidence=.7) as face:

                results = face.process(img)
                if results.detections:
                    for detection in results.detections:
                        #mp_draw.draw_detection(frame,detection)
                        detections = results.detections
                        loc = detections[0].location_data
                        bbox = loc.relative_bounding_box
                        x,y,iw,ih = bbox.xmin*w,bbox.ymin*h,bbox.width,bbox.height
                        cv2.rectangle(frame,(int(x),int(y)),(int(x+iw*w),int(y+h*ih)),(0,255,0),2)
                        cv2.circle(frame,(int((2*x+w*iw)/2),int((2*y+h*ih)/2)),5,(0,255,0),4)
                        cx,cy = int((2*x+w*iw)/2),int((2*y+h*ih)/2)
                        if abs(cx - prevcx) > 5:
                            angle = ((cx - 0)*((180-0)/(1080-0)) + 0) - 90
                            # print(angle)
                            command = str(angle)
                            # ard.write(command.encode())
                            # print(cx, prevcx, abs(cx-prevcx))
                        prevcx = cx
                            
        
        cv2.imshow("image",frame)     

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()
    cam.release()

class Brain():

    def __init__(self) -> None:
        pass

    def __call__(self, motor_control_input: list, params: list):
         for func, param in zip(motor_control_input, params):
            #   print(func)
              globals()[func[:func.index("(")]](param)

    def parse_parameter(self, funcs :list):
        params = []
        for param in funcs:
            bracket1 = param.index("(")
            bracket2 = param.index(")")

            var = param[bracket1+1:bracket2]
            params.append(var)
        # print(params)
        return params

    def parser(self, string:str):
        tokens=[]
        pattern=r'action\([^)]+\)'
        tokens = re.findall(pattern,string)
        tokens.extend(re.findall(r'emotion\([^)]+\)',string))
        actions=[]
        emotions=[]
        for i in tokens:
            if i.startswith("action"):
                process=i.partition("(")[2]
                obj=process.partition("(")[2]
                c=tokens.count("action(find("+obj)
                if c==0 and "find("+obj not in actions:
                    actions.append("find("+obj)
                    actions.append(process)
                else:
                    actions.append(i.partition("(")[2])
            elif i.startswith("emotion"):
                emotions.append(i.partition("(")[2][:-1])
        return actions,emotions
    
    def clean(self, string:str):
        return re.sub(r'\*\*[^*]*\*\*|\*[^*]*\*', '', string)

    def motor_control(self, inp : str):
        
        idx = inp.find("action:")
        # inp = inp[idx+len("action:"):].replace(" ","")
        actions = inp[idx+len("action:"):].split("**")
        actions.sort()
        actions.remove("")
        actions = list(filter((' ').__ne__, actions))
        print(actions)
        
        if actions[0] == '':
            return actions[1:]
        else:
            return actions
        
def user_interface():
        if BUFFER:
            print("Cow")
            image_window_test.FullScreenApp.fadeIn()
            image_window_test.FullScreenApp.updateText(BUFFER.pop())
        
def chat(msg:str):
    global initial_messages
    initial_messages.append(
            {"role":"user",
            "content":f"{msg}"}
        )
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=initial_messages,
        functions = functions,
        temperature=.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    resp = response['choices'][0]['message']['content']

    initial_messages.append(
        {"role":"assistant",
         "content":f"{resp}"}
    )
    return resp, response['choices'][0]['message']
    # print(f"chat: {msg}")  


def hi(msg:str):
    print(f"wave: {msg}")
    # ard.write(b'200')

def wave(msg:str):
    print(f"wave: {msg}")
    # ard.write(b'201')

def salute(msg:str):
    print(f"wave: {msg}")
    # ard.write(b'202')

def vqa(msg:str):
    print(f"vqa: {msg}")

def detect_obj(obj:str):
    print(f"detect_obj:{obj}")

def find(msg:str):
    print(f"find: {msg}")  

def grab(msg:str):
    print(f"grab: {msg}")

def place(obj:str):
    print(f"place:{obj}")

def happy():
    print("happy")
    # ard.write(b'500')

def angry():
    print("angry")
    # ard.write(b'600')
    
def sad():
    print("sad")
    # ard.write(b'700')

def neutral():
    print("neutral")

# Thread(target=eyes).start()
# Thread(target=user_interface).start()

# exit(0)
if __name__ ==  "__main__":
    B = Brain()
    whisp = STT()
    # bark = BarkSpeech()
    # Thread(target=head).start()
    mutex = 0
    BUFFER = []

    
    while True:
        try:
            voice = whisp.listen()
            msg = whisp.transcribe(voice)
            # msg = input(">>>")
            BUFFER.append(voice)
            print(msg)
            # os.system("cls")
            msg_l = msg.lower()
            if "ira" in msg_l or "aira" in msg_l or "ayra" in msg_l or "eira" in msg_l or 'era' in msg_l or "robot" in msg_l or 'robert' in msg_l:

                response, response_message = chat(msg)
                
                if response_message.get('function_call'):
                    
                    available_functions = {
                        "get_current_weather": get_current_weather
                    }  # only one function in this example, but you can have multiple
                    function_name = response_message["function_call"]["name"]
                    function_to_call = available_functions[function_name]
                    function_args = json.loads(response_message["function_call"]["arguments"])

                    function_response = function_to_call(
                        location=function_args.get("location"),
                        unit=function_args.get("unit"),
                    )

                    initial_messages.append(response_message)  # extend conversation with assistant's reply
                    initial_messages.append(
                        {
                            "role": "function",
                            "name": function_name,
                            "content": function_response,
                        }
                    )  # extend conversation with function response
                    second_response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo-0613",
                        messages=initial_messages,
                    )

                    initial_messages.append(
                        {"role":"assistant",
                        "content":f"{second_response['choices'][0]['message']['content']}"}
                    )

                    print("AIRA: ", second_response['choices'][0]['message']['content'])
                    engine.say(second_response['choices'][0]['message']['content'])
                    engine.runAndWait()
                    continue
                # Step 2: check if GPT wanted to call a function
                print("AIRA: ",response)
                actions, emotions = B.parser(response)

                if actions:
                    params = B.parse_parameter(actions)
                    B(actions, params)
                elif emotions:
                    print(emotions)
                    for emotion in emotions:
                        print("emotion",emotion)
                        globals()[emotion]()

                cleaned_response = B.clean(response)
                BUFFER.append(cleaned_response)
                # print("AIRA: ",cleaned_response)
                BUFFER.append((msg, cleaned_response))
                engine.say(cleaned_response)
                engine.runAndWait()
                # print(initial_messages)
        except Exception as e:
            print("error:", e)

  

    # thread1 = threading.Thread(target=main_process)
    # thread2 = threading.Thread(target=user_interface)
    # print("processes are starting")
    # thread1.start()
    # thread2.start()

    # thread1.join()
    # thread2.join()
    # print("Both tasks have completed.")