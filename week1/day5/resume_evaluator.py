import os
from dotenv import load_dotenv
from groq import Groq
from job_schema import schema , resume , final_score
from resume_reader import resume_parser

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=my_api_key)

job_json_schema = schema.model_json_schema()
resume_json_schema = resume.model_json_schema()
final_score_schema = final_score.model_json_schema()

model = "llama-3.3-70b-versatile"

system_prompt_job = f"""
You are an expert HR assistant. Your job is to extract details from job descriptions 
and output them strictly as a JSON object matching this schema: {job_json_schema}
Do not include any markdown formatting wrappers like ```json ... ```, and do not include conversational text.
"""

raw_job_description = """
Description
Do you want to solve real customer problems through innovative technology? Do you enjoy working on scalable services in a collaborative team environment? Do you want to see your code directly impact millions of customers worldwide?

At Amazon, we hire the best minds in technology to innovate and build on behalf of our customers. Customer obsession is part of our company DNA, which has made us one of the world's most beloved brands.

Our Software Development Engineers (SDEs) use modern technology to solve complex problems while seeing their work's impact first-hand. The challenges SDEs solve at Amazon are meaningful and influence millions of customers, sellers, and products globally. We seek individuals passionate about creating new products, features, and services while managing ambiguity in an environment where development cycles are measured in weeks, not years.

At Amazon, we believe in ownership at every level. As an SDE-I, you'll own the entire lifecycle of your code - from design through deployment and ongoing operations. This ownership mindset, combined with our commitment to operational excellence, ensures we deliver the highest quality solutions for our customers.

We're looking for curious minds who think big and want to define tomorrow's technology. At Amazon, you'll grow into the high-impact engineer you know you can be, supported by a culture of learning and mentorship. Every day brings exciting new challenges and opportunities for personal growth.
Key job responsibilities
• Collaborate and communicate effectively with experienced cross-disciplinary Amazonians to design, build, and operate innovative products and services that delight our customers, while participating in technical discussions to drive solutions forward.
• Design and develop scalable solutions using cloud-native architectures and microservices in a large distributed computing environment.
• Participate in code reviews and contribute to technical documentation.
• Build and maintain resilient distributed systems that are scalable, fault-tolerant, and cost-effective.
• Leverage and contribute to the development of GenAI and AI-powered tools to enhance development productivity while staying current with emerging technologies.
• Write clean, maintainable code following best practices and design patterns.
• Work in an agile environment practicing CI/CD principles while participating in operational responsibilities including on-call duties.
• Demonstrate operational excellence through monitoring, troubleshooting, and resolving production issues.
Basic Qualifications
- Experience with at least one general-purpose programming language such as Java, Python, C++, C#, Go, Rust, or TypeScript
- Experience with data structure implementation, basic algorithm development, and/or object-oriented design principles
- Currently has, or is in the process of obtaining a bachelor’s degree in Computer Science, Computer Engineering, Data Science, Information Systems, or related STEM fields
- Must be 18 years of age of older
Preferred Qualifications
- Experience from previous technical internship(s) or demonstrated project experience
- Experience with one or more of the following: AI tools for development productivity, Cloud platforms (preferably AWS), Database systems (SQL and NoSQL), Contributing to open-source projects, Version control systems, Debugging and troubleshooting complex systems
- Demonstrated ability to learn and adapt to new technologies quickly
- Basic understanding of software development lifecycle (SDLC)
- Strong problem-solving and analytical skills
- Excellent written and verbal communication skills"""

system_prompt_resume = f"""
You are an expert HR resume parser and data extraction assistant. 
Your job is to read the provided resume string and extract candidate details accurately, 
ignoring irrelevant filler, marketing fluff, or formatting artifacts.

You must parse the nested experience history correctly, capturing the company, role, duration (as an integer representing years), description, and skills for each job.

Output the extracted data strictly as a valid JSON object matching this schema: {resume_json_schema}
Do not include any markdown formatting wrappers like ```json ... ```, and do not include any conversational text.
"""

raw_resume_description = resume_parser.extract_file("resumes/abhay resume new - Abhay Singh.pdf")

message_system_job = {
    "role" : "system",
    "content" : system_prompt_job
}

message_user_job = {
    "role" : "user",
    "content" : raw_job_description
}

messages_job = [message_system_job, message_user_job]

message_system_resume = {
    "role" : "system",
    "content" : system_prompt_resume
}

message_user_resume = {
    "role" : "user",
    "content" : raw_resume_description
}

messages_resume = [message_system_resume, message_user_resume]


response_format = {
    "type" : "json_object"
}

response_job = client.chat.completions.create(
    model=model,
    messages=messages_job,
    temperature=0.0,
    response_format=response_format
)
response_resume = client.chat.completions.create(
    model=model,
    messages=messages_resume,
    temperature=0.0,
    response_format=response_format
)


json_string_job = response_job.choices[0].message.content
json_string_resume = response_resume.choices[0].message.content

job_data = schema.model_validate_json(json_string_job)
resume_data = resume.model_validate_json(json_string_resume)

print(job_data)
print(resume_data)

system_prompt_evaluator = f"""
You are an expert HR recruitment evaluator. Compare the candidate's resume JSON against the job description JSON.
Provide an overall match score (from 0 to 100) and place any qualitative analysis (such as name , email , matching skills, missing skills, and recommendations) inside the details dictionary.

Output the evaluation strictly as a JSON object matching this schema: {final_score_schema}
Do not include any markdown formatting wrappers like ```json ... ```, and do not include conversational text.
"""

user_prompt_comparison = f"""
### Job Description JSON:
{job_data}

### Candidate Resume JSON:
{resume_data}
"""

messages_evaluator = [
    {"role": "system", "content": system_prompt_evaluator},
    {"role": "user", "content": user_prompt_comparison},
]

response_evaluator = client.chat.completions.create(
    model=model,
    messages=messages_evaluator,
    temperature=0.0,
    response_format=response_format
)

json_string_score = response_evaluator.choices[0].message.content

score_data = final_score.model_validate_json(json_string_score)

print(score_data)

