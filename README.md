# AI Document Processing Service

## Setup
pip install -r requirements.txt
uvicorn app.main:app --reload

## Endpoints
- /validate
- /match
- /process

## Features
- Validation with confidence threshold
- Decision routing (auto / HITL / reject)
- Mock LLM-based commodity matching
- Audit trail logging

## Notes
- Used mock LLM for deterministic behavior
- Can be replaced with OpenAI/Groq API