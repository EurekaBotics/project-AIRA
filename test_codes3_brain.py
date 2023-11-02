import os
import re
import openai

openai.api_key = os.environ['API_KEY']

# def foo():
#     print("foooo")


# print(globals()['foo']())


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
    print(f"chat: {msg}")  

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

def wave(msg:str):
    print(f"wave:{msg}")

if __name__ ==  "__main__":

    B = Brain()
    string="Sure, I will arrange the boxes for you. **action(grab(red box))** **action(place(red box))** **action(grab(blue box))** **action(place(blue box))** **action(grab(green box))** **action(place(green box))** There you go, the boxes are now arranged in the order red, blue, green. Is there anything else I can assist you with? **emotion(neutral)** **action(wave())**"
    actions, emotions = B.parser(string)
    # print(actions, emotions)
    params = B.parse_parameter(actions)
    B(actions, params)



# actions = B.motor_control("Ok I will clean the table. action:**chat(msg)** **vqa(msg)** **detect_obj(object)**")
# params = B.parse_parameter(actions)
# B(actions, params)
# def parser(s:str):
#         act_count = s.count("action")
#         action_idx = []
#         idx = 0
#         for _ in range(act_count):
#             action_idx.append(s.index('action', idx))
#             idx = s.index('action')+1
#         return action_idx