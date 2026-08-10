import os
from dotenv import load_dotenv
from groq import Groq

from week1.day4.pydanticAndJson import response

load_dotenv()

my_api_key = os.getenv("MY_API_KEY")
client = Groq(api_key=my_api_key)
model = "llama-3.3-70b-versatile"

def llm_ans(prompt):
    message = {
        "role":"user",
        "content":prompt
    }
    messages = [message]
    response = client.chat.completions.create(
        model = model,
        messages=messages,
    )
    ans = response.choices[0].message.content
    return ans

basic_prompt = ("This is a user complaint"
                "phone not working "
                "classify this")
role_defined_prompt = ("You are a customer support assistant"
                       "you are provided with the query "
                       "phone not working"
                       "classify this")
task_defined_prompt = ("You are a customer support assistant"
                       "your task is to classify query of a customer"
                       "phone not working")
constraint_defined_prompt = ("You are a customer support assistant"
                             "your task is to classify query of a customer"
                             "the query can be only among the three (Billing,Technical,Return)"
                             "phone not working")
format_defined_prompt =  ("You are a customer support assistant"
                             "your task is to classify query of a customer"
                             "the query can be only among the three (Billing,Technical,Return)"
                             "you must provide one word ans"
                             "phone not working")
few_shot_prompt = ("You are a customer support assistant"
                             "your task is to classify query of a customer"
                             "the query can be only among the three (Billing,Technical,Return)"
                             "you must provide one word ans"
                             "for example if a user received wrong device : Return"
                             "for example if a user received wrong bill : Billing"
                             "for example if a user's device not working : Return"
                             "car not working")
fallback_defined_prompt = ("You are a customer support assistant"
                             "your task is to classify query of a customer"
                             "the query can be only among the three (Billing,Technical,Return)"
                             "you must provide one word ans"
                             "for example if a user received wrong device : Return"
                             "for example if a user received wrong bill : Billing"
                             "for example if a user's device not working : Return"
                             "if you are unable to relate the problem with the above categories u must return (I am not designed to solve such problems)"
                             "car not working")
print("-------------------------------------------------------------------------------------")
print(llm_ans(basic_prompt))
print("-------------------------------------------------------------------------------------")
print(llm_ans(role_defined_prompt))
print("-------------------------------------------------------------------------------------")
print(llm_ans(task_defined_prompt))
print("-------------------------------------------------------------------------------------")
print(llm_ans(constraint_defined_prompt))
print("-------------------------------------------------------------------------------------")
print(llm_ans(format_defined_prompt))
print("-------------------------------------------------------------------------------------")
print(llm_ans(few_shot_prompt))
print("-------------------------------------------------------------------------------------")
print(llm_ans(fallback_defined_prompt))
