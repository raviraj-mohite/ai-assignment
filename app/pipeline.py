from datetime import datetime
from app.validation import validate_envelope
from app.matching import match_commodity

async def process_envelope(env):
    errors, low_conf = validate_envelope(env)
    threshold = env.processing_instructions.confidence_threshold

    route = "auto_approve"

    if errors or low_conf:
        if env.processing_instructions.hitl_on_failure:
            route = "hitl_review"
        else:
            route = "rejected"

    env.validation_results = {
        "errors": errors,
        "low_confidence": low_conf
    }

    env.decision = {"route": route}

    env.audit.append({
        "timestamp": str(datetime.utcnow()),
        "action": "validation",
        "result": route
    })

    # matching if needed
    commodity = env.extraction.get("commodity_code")

    if commodity and commodity.confidence < threshold:
        desc = env.extraction.get("commodity_desc")

        if desc:
            result = match_commodity(desc.value)

            env.matching_results = result

            if result["match_confidence"] < 0.7:
                env.decision = {"route": "hitl_review"}

            env.audit.append({
                "timestamp": str(datetime.utcnow()),
                "action": "matching",
                "result": result["source"]
            })

    return env