# very rigid and not useful implementation

import os
from difflib import context_diff

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("MY_API_KEY")
client = Groq(api_key=my_api_key)
model = "llama-3.3-70b-versatile"

# step 1
knowledge_base = {
    "shaurya": "student of Manipal university jaipur",
    "age": "shaurya is 19",
    "educational background": "2 year in b-tech cse"
}


def retrieve_info(question):
    question = question.lower()
    if "shaurya" in question:
        return knowledge_base["shaurya"]
    elif "age" in question:
        return knowledge_base[question]
    elif "educational background" in question:
        return knowledge_base["educational background"]
    return None


def llm_ans(prompt_user):
    context = retrieve_info(prompt_user)

    message_system = {
        "role": "system",
        "content": f"""ans in one line only,
        and on the basis of context only do not hallucinate Context : {context}""",
    }
    message_user = {
        "role": "user",
        "content": prompt_user
    }
    messages = [message_system, message_user]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    ans = response.choices[0].message.content
    return ans


print(llm_ans("age of shaurya"))
