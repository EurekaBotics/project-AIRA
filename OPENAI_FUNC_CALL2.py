import openai
import os

openai.api_key = os.environ["API_KEY"]

def open_decorator(func):
    def wrapper():
        docs = func.__doc__
        name = func.__name__
        print("Wrapper")
        return {"name": name,
                "description": docs,
                "parameters":None}
    
    return wrapper



@open_decorator
def wave_hands():

    """Wave robots hands, when asked to say hi, or asked to wave hands."""

    print("wave hands")


f = wave_hands
print(f.__name__)
print(f.__doc__)
f()
# print(f.__globals__)





student_custom_functions = [
    {
        'name': 'extract_student_info',
        'description': 'Get the student information from the body of the input text',
        'parameters': {
            'type': 'object',
            'properties': {
                'name': {
                    'type': 'string',
                    'description': 'Name of the person'
                },
                'major': {
                    'type': 'string',
                    'description': 'Major subject.'
                },
                'school': {
                    'type': 'string',
                    'description': 'The university name.'
                },
                'grades': {
                    'type': 'integer',
                    'description': 'GPA of the student.'
                },
                'club': {
                    'type': 'string',
                    'description': 'School club for extracurricular activities. '
                }
                
            }
        }
    }
]














# def extract_docstring_content(func):
#     docstring = func.__doc__
#     if docstring:
#         # Split the docstring by triple quotes to get the content inside.
#         content = docstring.strip().strip('"""')
#         return content
#     else:
#         return None

# # Call the function to extract and print the content of its docstring
# content = extract_docstring_content(wave_hands)
# if content:
#     print("Docstring content:")
#     print(content)
# else:
#     print("No docstring found for the function.")
