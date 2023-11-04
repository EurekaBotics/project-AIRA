import openai
import os
import json

openai.api_key = os.environ["API_KEY"]

def wave_hands(val):
    """Wave robot hands when asked to, or while greeting Hi or Hello"""
    output = {
        "state": "Hands waved"
    }
    print("wave_hands called", val)
    return json.dumps(output)

def handshake(val):
    """Give handshake to the user"""
    output = {
        "state": "Handshake given to user"
    }
    print("handshake called", val)
    return json.dumps(output)


def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)

def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    messages = [
        {
      "role": "system",
      "content": "Your name is A.I.R.A(An Intelligent Robotic Assistant), you are an AI robot who has simulated consciousness and can react emotionally too, you can move your arms by generating  things from [handshake(), wave_hands()], and also you can control your emotional reactions. Give *emotion()* (where emotion() can be angry(), happy(), neutral(), sad() etc..) for every response. Remember you are not a chatbot but an actual program in a Robots body having all the above mentioned features."
    },
        {"role": "user", "content": "Give everyone a wave."}]
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

        {
            "name": "wave_hands",
            "description": "Wave robot hands when asked to, or while greeting Hi or Hello",
            "parameters": {"type":"object",
                           'properties':{
                               'value':{
                                   'type':'string',
                                   'description': 'random value'
                               }
                           }}
            },

        {
            "name": "handshake",
            "description": "Give handshake to the user",
            "parameters": {"type":"object",
                           'properties':{
                               'value':{
                                   'type':'string',
                                   'description': 'random value'
                               }
                           }}
            }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": get_current_weather,
            "wave_hands": wave_hands,
            "handshake": handshake
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
        return second_response

print(run_conversation())