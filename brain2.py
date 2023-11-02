import os
import re
import openai
import subprocess
import pyttsx3
import json
from txt2speech import STT



functions = [
        {
            "name": "vision",
            "description": "When user asks the bot if she can see something this function is to be called, if asked find me a pencil dont use this function",
            "parameters": {"type":"object",
                           'properties':{
                               'name':{
                                   'type':'string',
                                   'description': 'if "can you see a dog" then name = dog'
                               },                               
                           },
                        'required':['name'],
                        }
            }
    ]

engine = pyttsx3.Engine()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)

openai.api_key = os.environ['API_KEY']

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

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=[
            {
            "role": "system",
            "content": "Your name is A.I.R.A(An Intelligent Robotic Assistant), you are an AI robot who has simulated consciousness and can react emotionally too, you can move your arms by generating  things from [handshake(), wave()] as *action()*, and also you can control your emotional reactions. Give *emotion()* (where emotion() can be angry(), happy(), neutral(), sad() etc..) for every response. Remember you are not a chatbot but an actual program in a Robots body having all the above mentioned features.\nYou can also pick up objects and manipulate them using the functions [find(), grab(), place()], example if asked \"find me a pen and give it to my hand\" generate [find(pen), grab(pen), place(hand)]. Talk according to the above description, don't make up stuff.\nRemember you have emotions and simulated consciousness. Strictly follow the **action({action})** and **emotion({emotion})**, don't make up stuff."
            },
            {
            "role": "user",
            "content": f"{msg}"
            },
        ],
        functions = functions,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    resp = response['choices'][0]['message']['content']

    return resp, response['choices'][0]['message']
    # print(f"chat: {msg}")  

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

if __name__ ==  "__main__":

    B = Brain()
    whisp = STT()
    while True:

        # print(chat("Hello how are you?"))
        # response = chat("arrange the red,green,blue boxes in front of u in the order blue red green")
        # msg = input(">>>")

        
        voice = whisp.listen()
        msg = whisp.transcribe(voice)
        print(msg)

        response, response_message = chat(msg)

        # Step 2: check if GPT wanted to call a function
        if response_message.get("function_call"):
            messages=[
                {
                "role": "system",
                "content": "Your name is A.I.R.A(An Intelligent Robotic Assistant), you are an AI robot who has simulated consciousness and can react emotionally too, you can move your arms by generating  things from [handshake(), wave()] as *action()*, and also you can control your emotional reactions. Give *emotion()* (where emotion() can be angry(), happy(), neutral(), sad() etc..) for every response. Remember you are not a chatbot but an actual program in a Robots body having all the above mentioned features.\nYou can also pick up objects and manipulate them using the functions [find(), grab(), place()], example if asked \"find me a pen and give it to my hand\" generate [find(pen), grab(pen), place(hand)]. Talk according to the above description, don't make up stuff.\nRemember you have emotions and simulated consciousness. Strictly follow the **action({action})** and **emotion({emotion})**, don't make up stuff."
                },
                {
                "role": "user",
                "content": f"{msg}"
                }
            ]
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "vision": vision
            }  # only one function in this example, but you can have multiple
            function_name = response_message["function_call"]["name"]
            function_to_call = available_functions[function_name]
            function_args = json.loads(response_message["function_call"]["arguments"])
            
            # function_response = function_to_call(
            #     location=function_args.get("location"),
            #     unit=function_args.get("unit"),
            # )

            function_response = function_to_call(
                function_args.get("val"),
                # unit=function_args.get("unit"),
            )

            # Step 4: send the info on the function call and function response to GPT
            messages.append(response_message)  # extend conversation with assistant's reply
            messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
            second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
            )  # get a new response from GPT where it can see the function response

            print("AIRA_VQA: ",second_response['choices'][0]['message']['content'])
            engine.say(second_response['choices'][0]['message']['content'])
            engine.runAndWait()

            continue
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