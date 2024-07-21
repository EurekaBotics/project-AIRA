import os
import pyttsx3
from message import initial_messages, imposter_syndrome
from gui import FullScreenApp
from PyQt5.QtWidgets import QApplication
import sys
import queue, time, threading
from serial import Serial
from groq import Groq

# Disable section
disable_gui = False
disable_camera = True
disable_arduino = True

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
    ard = Serial("COM3", baudrate)  # Adjust if needed
    arduino_Thread = threading.Thread(
        target=ard_comm, args=(arduino_queue,), daemon=True
    )
    arduino_Thread.start()


class Brain:

    def __init__(self) -> None:
        self.engine = pyttsx3.Engine()
        self.voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", self.voices[1].id)
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )

    def generate(self, message):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "you are a helpful assistant."},
                {
                    "role": "user",
                    "content": "Explain the importance of fast language models",
                },
            ],
            model="llama3-8b-8192",
        )

        return print(chat_completion.choices[0].message.content)
