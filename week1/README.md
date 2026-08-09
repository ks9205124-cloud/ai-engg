# Week 1: Foundations of AI Engineering & Structured LLM Pipelines

Welcome to Week 1 of the AI Engineering repository! This week covers the foundational building blocks of working with Large Language Models (LLMs)—progressing from basic API initialization and real-time streaming to advanced structured outputs with Pydantic and building a full production-ready automated resume screening and ranking system.

## Directory Structure

```
week1/
├── day1/
│   └── hello_llm.py
├── day2/
│   └── streaming.py
├── day3/
│   └── tokens_sahurya.py
├── day4/
│   └── pydanticAndJson.py
├── day5/
│   ├── resumes/
│   ├── job_schema.py
│   ├── resume_evaluator.py
│   ├── resume_reader.py
│   └── main.py
├── .gitignore
└── pyproject.toml
```

## Daily Breakdown

### Day 1: Hello LLM (hello_llm.py)

**Focus:** Initializing the environment and making the first API call.

**Key Concepts:**

- Loading environment variables securely using python-dotenv.
- Initializing the Groq client (`Groq(api_key=...)`).
- Structuring a basic system/user prompt message payload and executing a chat completion request.

### Day 2: Streaming Responses (streaming.py)

**Focus:** Real-time text generation.

**Key Concepts:**

- Enabling streaming (`stream=True`) in API requests.
- Iterating through chunks as they arrive to deliver a responsive, typing-effect user experience.

### Day 3: Token Management (tokens_sahurya.py)

**Focus:** Token visibility and cost awareness.

**Key Concepts:**

- Inspecting response metadata to track prompt and completion token consumption.

### Day 4: Pydantic & Structured JSON (pydanticAndJson.py)

**Focus:** Deterministic and type-safe LLM outputs.

**Key Concepts:**

- Forcing LLMs into strict JSON mode (`response_format={"type": "json_object"}`).
- Using Pydantic (`BaseModel`) to validate model-generated data against explicit schemas.

### Day 5: Capstone Mini-Project (Automated Resume Screener & Ranker)

**Focus:** End-to-end multi-step AI workflow engineering.

**Key Components:**

- `resume_reader.py`: Extracts raw text from multi-format files (.pdf via pypdf and .docx via python-docx) using a robust utility handler.
- `job_schema.py`: Defines nested Pydantic schemas (experience, resume, job, and final_score) for type-safe data modeling.
- `main.py`: Orchestrates a batch pipeline that scans a folder of resumes, extracts candidate details, evaluates them against a target job description using dual-pass LLM calls, and outputs a ranked leaderboard of the top candidates.

## Getting Started

### 1. Clone and Navigate

```bash
git clone https://github.com/ks9205124-cloud/ai-engg.git
cd ai-engg/week1
```

### 2. Configure Environment Variables

Create a `.env` file in your root or project directory and add your Groq API key:

```
GROQ_API_KEY=your_actual_api_key_here
```

### 3. Install Dependencies

Install the required packages (Groq SDK, Pydantic, python-dotenv, pypdf, python-docx):

```bash
pip install .
# or if using poetry/uv/pip dependency management specified in pyproject.toml
```

### 4. Run the Day 5 Capstone Pipeline

To run the automated batch resume evaluator and rank your candidates:

```bash
python main.py
```