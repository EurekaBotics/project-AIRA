import json
import re

# import openai
import pyttsx3
import cv2
import mediapipe as mp
import threading
import queue
import time
import sys
from txt2speech import STT
from PyQt5.QtWidgets import QApplication
from groq import Groq
from gui import FullScreenApp
from WeatherAPI import *
from serial import Serial
from hotel_messages import initial_messages
import configparser
from VQA import GeminiVisionModel
from YoloModel import CalcPriceYolo
from print_color import print
from my_dataset import data

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

engine = pyttsx3.Engine()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

# AI model
# openai.api_key = OPENAI_KEY

# Disable section
disable_gui = True
disable_camera = True
disable_arduino = False

# GUI related
window = None


def run_gui():
    global window
    app = QApplication(sys.argv)
    window = FullScreenApp()
    window.showFullScreen()
    sys.exit(app.exec_())


# Camera realted
cam = None
debug_mode = False  # Prints the camera angle

# Arduino related
baudrate = 9600
arduino_queue = queue.Queue()
arduino_debug = 0  # Prints the content of queue if 1


def ard_comm(arduino_queue):
    global ard
    if ard:
        while True:
            while arduino_queue.empty():
                time.sleep(0.2)
                pass
            if arduino_debug:
                print("Contents of the queue:", list(arduino_queue.queue))
            code = arduino_queue.get() + "\n"
            ard.write(code.encode())

    else:
        print("ard not defined")


if not disable_arduino:
    ard = Serial("COM7", baudrate)  # Adjust if needed
    arduino_Thread = threading.Thread(
        target=ard_comm, args=(arduino_queue,), daemon=True
    )
    arduino_Thread.start()


class Brain:

    def __init__(self) -> None:
        pass

    def __call__(self, motor_control_input: list, params: list):
        for func, param in zip(motor_control_input, params):
            #   print(func)
            globals()[func[: func.index("(")]](param)

    def parse_parameter(self, funcs: list):
        params = []
        for param in funcs:
            bracket1 = param.index("(")
            bracket2 = param.index(")")

            var = param[bracket1 + 1 : bracket2]
            params.append(var)
        return params

    def parser(self, string: str):
        """
        Finds if action or emotion is present in the AI's answer.
        """
        tokens = []
        pattern = r"action\([^)]+\)"
        tokens = re.findall(pattern, string)
        tokens.extend(re.findall(r"emotion\([^)]+\)", string))
        actions = []
        emotions = []
        for i in tokens:
            if i.startswith("action"):
                process = i.partition("(")[2]
                obj = process.partition("(")[2]
                c = tokens.count("action(find(" + obj)
                if c == 0 and "find(" + obj not in actions:
                    actions.append("find(" + obj)
                    actions.append(process)
                else:
                    actions.append(i.partition("(")[2])
            elif i.startswith("emotion"):
                emotions.append(i.partition("(")[2][:-1])
        return actions, emotions

    def clean(self, string: str):
        return re.sub(r"\*\*[^*]*\*\*|\*[^*]*\*", "", string)

    def motor_control(self, inp: str):

        idx = inp.find("action:")
        # inp = inp[idx+len("action:"):].replace(" ","")
        actions = inp[idx + len("action:") :].split("**")
        actions.sort()
        actions.remove("")
        actions = list(filter((" ").__ne__, actions))
        print(actions)

        if actions[0] == "":
            return actions[1:]
        else:
            return actions


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
    """Get the current weather in the given location"""

    forecast = asyncio.run(getweather(location))
    weather_info = {"location": location, "forecast": forecast}
    return json.dumps(weather_info)


prevcx = 0
cx = 0


def eyes():
    global prevcx
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    mp_face = mp.solutions.face_detection
    mp_draw = mp.solutions.drawing_utils

    x = 0
    y = 0
    cx = 0
    cy = 0
    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                print("Error reading frame from the camera.")
                break
            h, w, c = frame.shape
            # print(h,w, c)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if cam.isOpened():
                with mp_face.FaceDetection(
                    model_selection=1, min_detection_confidence=0.7
                ) as face:

                    results = face.process(img)
                    if results.detections:
                        # mp_draw.draw_detection(frame,detection)
                        detections = results.detections
                        loc = detections[0].location_data
                        bbox = loc.relative_bounding_box
                        x, y, iw, ih = (
                            bbox.xmin * w,
                            bbox.ymin * h,
                            bbox.width,
                            bbox.height,
                        )

                        cv2.rectangle(
                            frame,
                            (int(x), int(y)),
                            (int(x + iw * w), int(y + h * ih)),
                            (0, 255, 0),
                            2,
                        )
                        cv2.circle(
                            frame,
                            (int((2 * x + w * iw) / 2), int((2 * y + h * ih) / 2)),
                            5,
                            (0, 255, 0),
                            4,
                        )

                        cx, cy = int((2 * x + w * iw) / 2), int((2 * y + h * ih) / 2)
                        angle = (cx - 0) * ((180 - 70) / (1080 - 0)) + 0

                        if abs(prevcx - angle) > 10:
                            command = str(int(angle))
                            if debug_mode:
                                print(f"camera: {command}")
                            prevcx = angle
                            arduino_queue.put(command)

            cv2.imshow("image", frame)

            if cv2.waitKey(1) == ord("q"):
                break

    except Exception as e:
        print(e)

    finally:
        cv2.destroyAllWindows()
        cam.release()


# Openai
# def chat(msg: str):
#     global initial_messages
#     initial_messages.append({"role": "user", "content": f"{msg}"})
#     response = openai.ChatCompletion.create(
#         model="gpt-4-0613",
#         messages=initial_messages,
#         # messages=imposter_syndrome,
#         functions=functions,
#         temperature=0.7,
#         max_tokens=256,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0,
#     )

#     resp = response["choices"][0]["message"]["content"]

#     initial_messages.append({"role": "assistant", "content": f"{resp}"})
#     return resp, response["choices"][0]["message"]
#     # print(f"chat: {msg}")


def chat(msg: str):
    global initial_messages
    initial_messages.append({"role": "user", "content": f"{msg}"})
    response = client.chat.completions.create(
        messages=initial_messages,
        model="llama3-70b-8192",
    )

    resp = response.choices[0].message.content
    initial_messages.append({"role": "assistant", "content": f"{resp}"})
    return resp, response.choices[0].message
    # print(f"chat: {msg}")


def hi(msg):
    print(f"hi")
    arduino_queue.put("200")


def wave(msg):
    print(f"wave")
    arduino_queue.put("201")


def salute(msg):
    print(f"salute:")
    arduino_queue.put("202")


def vqa(msg: str):
    print(f"vqa: {msg}")
    vqa = GeminiVisionModel()
    return vqa.perform_vqa(msg)


def detect_obj(obj: str):
    print(f"detect_obj:{obj}")


def calculate_price():
    model = CalcPriceYolo()
    val = model.perform_object_detection()
    return f"Total money calculated from the image is {val}"


def find(msg: str):
    print(f"find: {msg}")


def grab(msg: str):
    print(f"grab: {msg}")


def place(obj: str):
    print(f"place:{obj}")


def happy():
    print("happy")
    arduino_queue.put("302")


def sad():
    print("sad")
    arduino_queue.put("303")


def angry():
    print("angry")
    arduino_queue.put("304")


def neutral():
    print("neutral")


def confused():
    print("confused")
    arduino_queue.put("305")


def surprised():
    print("surprised")
    arduino_queue.put("306")


if not disable_camera:
    Thread = threading.Thread(target=eyes, daemon=True)
    Thread.start()

if not disable_gui:
    gui_thread = threading.Thread(target=run_gui, daemon=True)
    gui_thread.start()

if __name__ == "__main__":

    if sys.platform.startswith("linux"):
        print("Initilizing AIRA in Linux Env")
    elif sys.platform.startswith("win"):
        print("Initilizing AIRA in Windows")
    elif sys.platform.startswith("macOS"):
        print("Initilizing AIRA in mac")
    else:
        print("Initilizing AIRA in Unknown OS")

    B = Brain()
    whisp = STT()
    count = 0
    while True:
        try:
            if not disable_gui:
                window.text_simulation_thread.set_text_to_simulate(f"Listening...")
            voice = whisp.listen()
            if not disable_gui:
                window.text_simulation_thread.set_text_to_simulate(f"Processing...")
            msg = whisp.transcribe(voice)
            msg_l = msg.lower()
            if "robert" in msg_l:
                msg_l = msg_l.replace("robert", "robot")
                print("hi")
            count += 1
            if count == 2:
                count = 0
                initial_messages = initial_messages

            print(f"Human: {msg_l}")
            if (
                "ira" in msg_l
                or "aira" in msg_l
                or "ayra" in msg_l
                or "eira" in msg_l
                or "robot" in msg_l
                or "robert" in msg_l
                or "robo" in msg_l
            ):
                if not disable_gui:
                    window.text_simulation_thread.set_text_to_simulate(
                        f"Human: {msg_l}"
                    )
                response, response_message = chat(msg_l)

                if response_message.function_call:

                    available_functions = {"get_current_weather": get_current_weather}
                    function_name = response_message["function_call"]["name"]
                    function_to_call = available_functions[function_name]
                    function_args = json.loads(
                        response_message["function_call"]["arguments"]
                    )

                    function_response = function_to_call(
                        location=function_args.get("location"),
                        unit=function_args.get("unit"),
                    )

                    initial_messages.append(response_message)
                    initial_messages.append(
                        {
                            "role": "function",
                            "name": function_name,
                            "content": function_response,
                        }
                    )
                    # second_response = openai.ChatCompletion.create(
                    #     model="gpt-3.5-turbo-0613",
                    #     messages=initial_messages,
                    # )

                    second_response = client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=initial_messages,
                    )

                    initial_messages.append(
                        {
                            "role": "assistant",
                            "content": f"{second_response.choices[0].message.content}",
                        }
                    )

                    print("AIRA: ", second_response.choices[0].message.content)
                    engine.say(second_response.choices[0].message.content)
                    engine.runAndWait()
                    continue

                print("AIRA: ", response)

                actions, emotions = B.parser(response)
                vqa_exists = False
                price_exists = False
                if actions:
                    print("action called")
                    params = B.parse_parameter(actions)
                    vqa_pattern = re.compile(r"vqa\((.*?)\)")
                    for action in actions:
                        match = vqa_pattern.search(action)
                        if match:
                            vqa_exists = True
                            vqa_query = match.group(1).strip("'\"")
                            out = vqa(vqa_query)
                            engine.say(out)
                            print(out, color="red")
                            engine.runAndWait()
                            break
                    if not vqa_exists:
                        print("no vqa loop")
                        price_pattern = re.compile(r"price\((.*?)\)")
                        for action in actions:
                            match = price_pattern.search(action)
                            if match:
                                price_exists = True
                                price_query = match.group(1).strip("'\"")
                                price = calculate_price()
                                print(f"Calculated Price: {price}", color="green")
                                break
                        if not price_exists:
                            print("no price_exist loop")
                            params = B.parse_parameter(actions)
                            B(
                                actions, params
                            )  # this is a __call__ enabled function that does something that noone knows
                            print(actions, color="red")
                            engine.runAndWait()

                            # cleaned_response = B.clean(response)
                            # engine.say(cleaned_response)

                if emotions:
                    print(emotions)
                    for emotion in emotions:
                        print("emotion", emotion)
                        globals()[emotion]()
                if not vqa_exists:
                    cleaned_response = B.clean(response)
                    engine.say(cleaned_response)
                if not disable_gui:
                    window.text_simulation_thread.set_text_to_simulate(
                        f"AIRA: {cleaned_response}" + "\n"
                    )
                engine.runAndWait()

        except KeyboardInterrupt:
            gui_thread.join()
            break

        except Exception as e:
            print("error:", e)

# test
