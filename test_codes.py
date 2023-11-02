import re

# Define the mixed-up text
mixed_up_text = "Sure, I will arrange the boxes for you. **action(grab(red box))** *action(place(red box))* *action(grab(blue box))* **action(place(blue box))** **action(green box)** *action(place(green box))* There you go, the boxes are now arranged in the order red, blue, green. *emotion(neutral)*"

# Remove text enclosed in **{}** or *{}* using regular expressions
normal_text = re.sub(r'\*\*[^*]*\*\*|\*[^*]*\*', '', mixed_up_text)

# Print the extracted normal text
print(normal_text)
