import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

from week1.day1.hello_llm import message

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("Environment variable GROQ_API_KEY_API_KEY must be set")

client = Groq(api_key=my_api_key)
model = "llama-3.3-70b-versatile"
role = "user"

content = "write a 100 line output explaining streaming"

message = {
    "role": role,
    "content": content
}

messages = [message]

response = client.chat.completions.create(model=model,messages=messages,stream=True)

for chunk in response:
    content = chunk.choices[0].delta.content
    if content :
        print(content,end="",flush=True)
