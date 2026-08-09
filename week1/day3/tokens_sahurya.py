import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("MY_API_KEY")
client = Groq(api_key=my_api_key)

model = "llama-3.3-70b-versatile"
role = "user"

# 1. Store prompts as plain strings (no set braces {})
prompt1 = "hello"
prompt2 = "make a gist This is a tutorial project on token give a gist of this project"
prompt3 = "Write a 1000 letter description over prompt engineering"

prompts = [prompt1, prompt2, prompt3]

# 2. Indent everything inside the loop to run an API call for each prompt
for prompt in prompts:
    print(f"\n\n==================== Output for prompt: '{prompt}' ====================\n")

    messages = [
        {
            "role": role,
            "content": prompt,
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=50
    )
    usage = response.usage
    print(f"Prompt: {prompt} --> your token {usage.prompt_tokens} completion token {usage.completion_tokens}")

usage = response.usage
print(response.choices[0].message.content)
print(f"\n[Tokens Used] Prompt: {usage.prompt_tokens} | Completion: {usage.completion_tokens} | Total: {usage.total_tokens}")