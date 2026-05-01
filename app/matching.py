def match_commodity(desc: str):
    desc = desc.lower()

    if "computer" in desc:
        return {
            "matched_code": "8471",
            "match_confidence": 0.85,
            "rationale": "Matched keyword 'computer'",
            "fallback_used": True,
            "source": "llm_match"
        }

    if "phone" in desc:
        return {
            "matched_code": "8517",
            "match_confidence": 0.80,
            "rationale": "Matched keyword 'phone'",
            "fallback_used": True,
            "source": "llm_match"
        }

    return {
        "matched_code": None,
        "match_confidence": 0.0,
        "rationale": "No match found",
        "fallback_used": False,
        "source": "no_match"
    }