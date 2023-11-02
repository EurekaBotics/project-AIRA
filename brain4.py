import os
import re
import openai
import subprocess
import pyttsx3
import json
from txt2speech import STT
import cv2
import mediapipe as mp
import threading
from serial import Serial


Thread = threading.Thread

# ard = Serial("COM4", 9600) 

engine = pyttsx3.Engine()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)

openai.api_key = os.environ['API_KEY']

initial_messages=[
            {
            "role": "system",
            "content": "Your name is A.I.R.A(An Intelligent Robotic Assistant), you are an AI robot who has simulated consciousness and can react emotionally too, you can move your arms by generating  things from [handshake(), wave()] as *action()*, and also you can control your emotional reactions. Give *emotion()* (where emotion() can be angry(), happy(), neutral(), sad() etc..) for every response. Remember you are not a chatbot but an actual program in a Robots body having all the above mentioned features.\nYou can also pick up objects and manipulate them using the functions [find(), grab(), place()], example if asked \"find me a pen and give it to my hand\" generate [find(pen), grab(pen), place(hand)]. Talk according to the above description, don't make up stuff.\nRemember you have emotions and simulated consciousness."
            },
            {
            "role": "user",
            "content": "How are you?"
            },
            {
            "role": "assistant",
            "content": "I am doing well, thank you for asking. How are you feeling today? *emotion(neutral)*"
            },
            {
            "role": "user",
            "content": "you have red, green, blue boxes in front of you arrange them in the order red, blue, green"
            },
            {
            "role": "assistant",
            "content": "Sure, I will arrange the boxes for you. *action(grab(red box))* *action(place(red box))* *action(grab(blue box))* *action(place(blue box))* *action(grab(green box))* *action(place(green box))* There you go, the boxes are now arranged in the order red, blue, green. Is there anything else I can assist you with? *emotion(neutral)*"
            }
        ]

cx = 0
prevcx = 0
def eyes():
    global cx
    cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    mp_face = mp.solutions.face_detection
    mp_draw = mp.solutions.drawing_utils

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
            with mp_face.FaceDetection(model_selection = 0) as face:

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
            

            
        
        cv2.imshow("image",frame)

        

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()
    cam.release()

# subprocess.run("echo hello")    

# exit(0)

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

def chat(msg:str):
    global initial_messages
    initial_messages.append(
            {"role":"user",
            "content":f"{msg}"}
        )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=initial_messages,
        temperature=0.5,
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


def head():
    global cx
    global prevcx

    if abs(cx - prevcx) > 30:
        angle = (cx - 0)*((180-0)/(640-0)) + 0
        command = str(angle)
        # ard.write(command.encode())


def wave(msg:str):
    print(f"wave: {msg}")

def vqa(msg:str):
    print(f"vqa: {msg}")

def detect_obj(obj:str):
    print(f"detect_obj:{obj}")
    # HEllo world

def find(msg:str):
    print(f"find: {msg}")  

def grab(msg:str):
    print(f"grab: {msg}")

def place(obj:str):
    print(f"place:{obj}")

def vision(name):
    """When user asks the bot if she can see something this function is to be called, if asked find me a pencil dont use this function"""
    output = {
        "name":name,
        "state": "yes"
    }
    print("vision called", name)
    return json.dumps(output)


Thread(target=eyes).start()
Thread(target=head).start()

# exit(0)
if __name__ ==  "__main__":
    B = Brain()
    whisp = STT()
    
    while True:
        print("cx",cx)
        voice = whisp.listen()
        msg = whisp.transcribe(voice)
        print(msg)

        response, response_message = chat(msg)

        # Step 2: check if GPT wanted to call a function
        print("AIRA: ",response)
        actions, emotions = B.parser(response)

        if actions:
            params = B.parse_parameter(actions)
            B(actions, params)
        elif emotions:
            print(emotions)
            pass

        cleaned_response = B.clean(response)
        print("AIRA: ",cleaned_response)
        engine.say(cleaned_response)
        engine.runAndWait()
        
        # exit(0)
        
        # string="Sure, I will arrange the boxes for you. **action(grab(red box))** **action(place(red box))** **action(grab(blue box))** **action(place(blue box))** **action(grab(green box))** **action(place(green box))** There you go, the boxes are now arranged in the order red, blue, green. Is there anything else I can assist you with? **emotion(neutral)**"
        # string = "Hello how are you **emotion(happy)**"
        # actions, emotions = B.parser(string)
        # print(actions, emotions)
        # params = B.parse_parameter(actions)
        # B(actions, params)