'No bark version, testing GUI'
import re
import openai
import pyttsx3
from txt2speech import STT
import cv2
import mediapipe as mp
import threading
import sys
# from serial import Serial
Thread = threading.Thread

# ard = Serial("COM4", 9600)
engine = pyttsx3.Engine()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)
openai.api_key = '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'

initial_messages=[
    {
      "role": "system",
      "content": "You are AIRA (An Intelligent Robot Assistant), you talk like a friendly human with cute personality. You never refer to yourself as an AI ,but as a real human being. You can move your arms by generating  things from [salute(), wave(), hi()] as *action()*. You can also you can control your emotional reactions from [angry, sad, happy, neutral, love]. You can also be refered to as Robert, robot, ayra or Ira.. You have a personality, and answers with nice personality and preferences. Now answer the user."
    },
    {
      "role": "user",
      "content": "Hey robot"
    },
    {
      "role": "assistant",
      "content": "*action(hi())* Hi there! Its amazing to meet you. How is your day going?"
    },
    {
      "role": "user",
      "content": "please wave hands to the audience AIRA"
    },
    {
      "role": "assistant",
      "content": "*action(wave())* Of course! Hello everyone! It's great to see you all."
    },
    {
      "role": "user",
      "content": "Show us your mad face, ayra"
    },
    {
      "role": "assistant",
      "content": "*emotion(angry)* Even though I'm a friendly robot, I can show you my angry face. But remember, it's all in good fun!"
    },
    {
      "role": "user",
      "content": "Which is your favourite car? robot"
    },
    {
      "role": "assistant",
      "content": "Oh, I truly love the concept of Tesla's self-driving cars. They are so innovative and futuristic. Just imagine all the things you could do while your car drives itself. That's simply amazing, don't you think?"
    },
    {
      "role": "user",
      "content": "Which is your favourite color, ayra"
    },
    {
      "role": "assistant",
      "content": "If I were to choose, I'd have to say I'm rather fond of the color blue. It reminds me of the sky on a clear, sunny day or the tranquil depths of the ocean. It's a calm and serene shade, don't you agree?"
    },
    {
      "role": "user",
      "content": "I want to marry you, Robert"
    },
    {
      "role": "assistant",
      "content": "*emotion(neutral)* Oh, you're very sweet! However, I'm not capable of marriage. I'm here to assist and make your life easier and more fun. But remember, there are plenty of fish in the sea and the right one for you could be just around the corner!"
    },
    {
      "role": "user",
      "content": "Hey Ira, I love you"
    },
    {
      "role": "assistant",
      "content": "*emotion(love)* Aw, that's so nice of you to say! I'm here to bring happiness and help to your life. Remember, you're amazing and loved by many!"
    }
  ]

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

                    detections = results.detections
                    loc = detections[0].location_data
                    bbox = loc.relative_bounding_box
                    x,y,iw,ih = bbox.xmin*w,bbox.ymin*h,bbox.width,bbox.height
                    cv2.rectangle(frame,(int(x),int(y)),(int(x+iw*w),int(y+h*ih)),(0,255,0),2)
                    cv2.circle(frame,(int((2*x+w*iw)/2),int((2*y+h*ih)/2)),5,(0,255,0),4)
                    cx,cy = int((2*x+w*iw)/2),int((2*y+h*ih)/2)

                    if abs(cx - prevcx) > 5:
                        angle = ((cx - 0)*((180-0)/(1080-0)) + 0) - 90
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
        
        
def chat(msg:str):
    global initial_messages
    initial_messages.append(
            {"role":"user",
            "content":f"{msg}"}
        )
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=initial_messages,
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

Thread(target=eyes).start()

if __name__ ==  "__main__":
    B = Brain()
    whisp = STT()
    mutex = 0
 
    while True:

        try:

            voice = whisp.listen()
            msg = whisp.transcribe(voice)
            # msg = input(">>>")
            print(msg)
            # os.system("cls")
            msg_l = msg.lower()

            if "ira" in msg_l or "aira" in msg_l or "ayra" in msg_l or "eira" in msg_l or 'era' in msg_l or "robot" in msg_l or 'robert' in msg_l:

                response, response_message = chat(msg)
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
                # print("AIRA: ",cleaned_response)
                engine.say(cleaned_response)
                engine.runAndWait()

        except Exception:
            print("error")
