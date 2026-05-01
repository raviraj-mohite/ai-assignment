from pydantic import BaseModel
from typing import Optional, Dict, List

class FieldData(BaseModel):
    value: Optional[str]
    confidence: Optional[float]

class ProcessingInstructions(BaseModel):
    confidence_threshold: float
    hitl_on_failure: bool

class Envelope(BaseModel):
    envelope_id: str
    extraction: Dict[str, FieldData]
    processing_instructions: ProcessingInstructions

    validation_results: Optional[Dict] = None
    matching_results: Optional[Dict] = None
    decision: Optional[Dict] = None
    audit: List[Dict] = []