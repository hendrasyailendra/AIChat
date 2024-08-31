import json
import random


def get_recent_messages():
    file_name = "stored_data.json"
    learn_instruction = {
        "role": "system",
        "content": "You are interviewing customer to fill in a form. Keep your answer to under 30 words."
    }

    messages = []

    x = random.uniform(0,1)
    if x < 0.5 :
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include some dad jokes"
    else :
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include a critical question"

    messages.append(learn_instruction)

    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

        if data:
            if len(data) < 5:
                for item in data:
                    messages.append(item)
            else:
                for item in data[-5]:
                    messages.append(item)
    except Exception as e:
        print(e)
        pass

    return messages

def store_messages(request_message, response_message):
    
    file_name = "stored_data.json"
    messages = get_recent_messages()[1:]

    user_messages = {"role":"user", "content": request_message}
    assistant_messages = {"role":"assistant", "content": response_message}
    messages.append(user_messages)
    messages.append(assistant_messages)

    with open(file_name, "w") as f:
        json.dump(messages, f)

def reset_message():
    open("stored_data.json","w")