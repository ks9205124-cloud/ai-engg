import os
from email import message
from pathlib import Path
from urllib import response

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("Environment variable GROQ_API_KEY is not set")

client = Groq(api_key=my_api_key)
model = "llama-3.3-70b-versatile"
role = "user"

prompt = "do u know ryan pinto"

message = {
    "role" : role,
    "content" : prompt,
}

messages = [message]

response = client.chat.completions.create(model=model,messages=messages)

print(response.choices[0].message.content)