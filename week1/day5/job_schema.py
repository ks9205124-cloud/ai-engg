from pydantic import BaseModel

class schema(BaseModel):
    role: str
    req_skill: str
    preffered_skill: str
    minimum_experience: int
    education_requirements: str
    responsibilities: str

class experience(BaseModel):
    company: str
    role: str
    duration: int
    description: str
    skill: str

class resume(BaseModel):
    name: str
    email: str
    phone_number: str
    total_experience: int
    skill: list[str]
    experiences: list[experience]
    project: list[str]
    certifications: list[str]

class final_score(BaseModel):
    score: int
    details: dict
