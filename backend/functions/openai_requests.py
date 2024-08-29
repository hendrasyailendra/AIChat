import json

import openai
import requests
from decouple import config
from functions.database import get_recent_messages

# Retrieve Enviornment Variables
openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")
apiKey = config("API_KEY")
whisperUrl = "https://hackathonopenai-instance.openai.azure.com/openai/deployments/whisper-hackathon-test/audio/translations?api-version=2024-06-01"
gptUrl = "https://hackathonopenai-instance.openai.azure.com/openai/deployments/Hackathon-GPT4o/chat/completions?api-version=2023-03-15-preview"

# Convert audio to text
def convert_audio_to_text(audio_file):
  try:
    #transcript = openai.Audio.transcribe("whisper-1", audio_file)
    files = {'file': audio_file}
    headers = {"api-key": apiKey}
    response = requests.post(whisperUrl, headers=headers, files=files)
    message = json.loads(response.text)
    print(message['text'])
    return message['text']
  except Exception as e:
    print(e)
    return
  
def get_chat_response(message_input):
  messages = get_recent_messages()
  user_message = {"role": "user", "content": message_input }
  messages.append(user_message)
  try:
    headers = {"api-key": apiKey}
    data={"messages": messages}
    response = requests.post(gptUrl, headers=headers, json=data)
    print(response.json())
    message = json.loads(response.text)
    return message["choices"][0]["message"]["content"]
  except Exception as e:
    return