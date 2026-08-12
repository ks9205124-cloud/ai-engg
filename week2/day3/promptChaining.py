import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

my_api_key = os.getenv("MY_API_KEY")
client = Groq(api_key=my_api_key)
model = "llama-3.3-70b-versatile"

def llm_ans(prompt_system,prompt_user):
    message_system = {
        "role" : "system",
        "content" : prompt_system,
    }
    message_user = {
        "role":"user",
        "content":prompt_user
    }
    messages = [message_system,message_user]
    response = client.chat.completions.create(
        model = model,
        messages=messages,
    )
    ans = response.choices[0].message.content
    return ans


JD="""
We are hiring a Backend Python Developer.

Requirements:
- Strong Python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
- REST APIs
- 2+ years of experience
"""
RESUME="""
Name: Rahul Sharma

Experience:
3 years as a Software Developer.

Skills:
Python, FastAPI, MySQL, Docker,
REST APIs, Git

Projects:
Built a food delivery backend using
FastAPI and MySQL.

Deployed applications using Docker.
"""

# this is example script made to use the concept of prompt chaining



def extract_skills_from_resume():
    system_prompt = """
    role: you are a text extraction tool
    task: extract skills from sample resume provided
    constraints: you must extract all the skills from resume provided and must not hallucinate anything on your end
    output format: create a list of skills in such a format: ['skill1','skill2','skill3']
    fallback: if no skill found return a list ['bad_hire']
    """

    user_prompt = f"""
    extract skills from resume provided
    {RESUME}
    """

    return llm_ans(system_prompt,user_prompt)

def extract_skills_from_jd():
    system_prompt = """
    role: you are a text extraction tool
    task: extract skills from sample JD provided
    constraints: you must extract all the skills from JD provided and must not hallucinate anything on your end
    output format: create a list of skills in such a format: ['skill1','skill2','skill3']
    fallback: if no skill found return a list ['bad_hire']
    """

    user_prompt = f"""
    extract skills from JD provided
    {JD}
    """

    return llm_ans(system_prompt,user_prompt)

def match_skills(skill_resume,skill_jd):
    system_prompt = """
        role: you are a HR assistant tool
        task: match skills from sample JD and resume provided
        constraints: you must match all the skills from JD and resume provided and consider a small advantage for additional skills if any
        output format: create a score btw 0 to 100 
                        must provide the list of skill matched ['match_skill1','match_skill2','match_skill3'] 
                        must provide list of skill not matched ['no_match_skill1','no_match_skill2','no_match_skill3']
                        must provide a list of additional skill ['additional_skill1','additional_skill2','additional_skill3']
                        finally a short verdict weather the user is fit for the role or not
        fallback: if no skill found return a list ['bad_hire']
        """

    user_prompt = f"""
        JD: {skill_jd}
        Resume: {skill_resume}
        """

    return llm_ans(system_prompt,user_prompt)

candidate_skill = (extract_skills_from_resume())

jd_skill = (extract_skills_from_jd())

print(match_skills(candidate_skill,jd_skill))