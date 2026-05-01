from fastapi import FastAPI, HTTPException
from app.models import Envelope
from app.validation import validate_envelope
from app.matching import match_commodity
from app.pipeline import process_envelope

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok", "service": "ai-assignment", "version": "1.0"}


@app.post("/validate")
async def validate(env: Envelope):
    errors, low_conf = validate_envelope(env)

    if errors:
        raise HTTPException(status_code=422, detail=errors)

    route = "auto_approve"

    if low_conf:
        if env.processing_instructions.hitl_on_failure:
            route = "hitl_review"
        else:
            route = "rejected"

    env.validation_results = {
        "errors": errors,
        "low_confidence": low_conf
    }

    env.decision = {"route": route}

    return env


@app.post("/match")
async def match(env: Envelope):
    desc = env.extraction.get("commodity_desc")

    if desc:
        result = match_commodity(desc.value)
        env.matching_results = result

        if result["match_confidence"] < 0.7:
            env.decision = {"route": "hitl_review"}

    return env


@app.post("/process")
async def process(env: Envelope):
    return await process_envelope(env)