from datetime import datetime, timedelta

def validate_envelope(env):
    errors = []
    low_conf = []

    threshold = env.processing_instructions.confidence_threshold

    # required fields
    required = ["shipment_id", "recipient_name"]

    for field in required:
        if field not in env.extraction or not env.extraction[field].value:
            errors.append(f"{field} missing")

    # confidence check
    for key, field in env.extraction.items():
        if field.confidence is not None and field.confidence < threshold:
            low_conf.append(key)

    # date validation
    if "ship_date" in env.extraction:
        try:
            date = datetime.fromisoformat(env.extraction["ship_date"].value)
            if date > datetime.now():
                errors.append("ship_date in future")
            if date < datetime.now() - timedelta(days=365):
                errors.append("ship_date too old")
        except:
            errors.append("invalid date format")

    return errors, low_conf