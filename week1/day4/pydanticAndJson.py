import os
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, schema

load_dotenv()

class ticket(BaseModel):
    name: str
    email: str
    category: str

schema = ticket.model_json_schema()

response_format = {
    "type" : "json_object"
}


system_prompt = f"""Extract the user's information and return a JSON object strictly matching this schema: {schema}"""

message_system = {
    "role" : "system",
    "content" : system_prompt
}

text = "Hi, my name is Jane Doe (jane@example.com). I want to submit a complaint about my bill."

message_user = {
    "role" : "user",
    "content" : text
}

messages = [message_system,message_user]

my_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=my_api_key)

model = "llama-3.3-70b-versatile"

response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0.0,                  # Lower temperature for strict structure
    response_format=response_format   # Forces valid raw JSON output
)

# Extract raw string
json_string = response.choices[0].message.content
print("Raw API Output:")
print(json_string)

import json
raw_json = json_string
data_file = json.loads(raw_json)
Ticket = ticket(**data_file)

print(Ticket.name)
print(Ticket.email)
print(Ticket.category)


