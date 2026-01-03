from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import List, Dict
import re

# Assuming you saved the previous code as governance_engine.py
from governance_engine import AegisShield 

app = FastAPI(title="Aegis Enterprise AI Gateway")

# 1. CORS Configuration (The Browser Shield)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Governance Engine
shield = AegisShield()

# 2. Policy Definitions (Corporate Guardrails)
DENIED_KEYWORDS = ["salary", "password", "social security", "secret key", "blueprint"]

class AIRequest(BaseModel):
    user_id: str
    dept: str
    prompt: str

    # Pydantic Validator: Stops restricted content before it hits the NLP model
    @field_validator('prompt')
    @classmethod
    def check_policy_violations(cls, v: str) -> str:
        text_lower = v.lower()
        for word in DENIED_KEYWORDS:
            if word in text_lower:
                # In Enterprise apps, we raise a 422 for policy violations
                raise ValueError(f"Security Violation: Restricted content found ('{word}')")
        return v

def calculate_risk_score(original: str, sanitized: str) -> Dict:
    """Architect's Note: Measures how 'toxic' or 'sensitive' the prompt was."""
    # Count how many tags (e.g., <PERSON>) were inserted
    tags_found = len(re.findall(r'<[A-Z_]+>', sanitized))
    
    score = min(tags_found * 20, 100) # Simple linear risk scaling
    
    if score == 0:
        level = "CLEAN"
    elif score < 40:
        level = "LOW"
    elif score < 80:
        level = "MEDIUM"
    else:
        level = "CRITICAL"
        
    return {"score": score, "level": level, "redactions": tags_found}

@app.get("/")
def health_check():
    return {"status": "Aegis Online", "version": "1.2.0", "engine": "spaCy 3.8.11"}

@app.post("/v1/gate")
async def process_request(request: AIRequest):
    try:
        # Step 1: Governance Step - Mask PII
        sanitized_prompt = shield.protect_prompt(request.prompt)
        
        # Step 2: Risk Assessment - Quantify the Danger
        risk_data = calculate_risk_score(request.prompt, sanitized_prompt)
        
        # Step 3: Architect's Gateway Response
        return {
            "status": "success",
            "risk_assessment": risk_data,
            "governance_report": {
                "original_prompt": request.prompt,
                "sanitized_prompt": sanitized_prompt,
                "applied_policies": ["PII_REDACTION", "KEYWORD_FILTERING"]
            },
            "metadata": {
                "dept": request.dept,
                "user": request.user_id,
                "action": "REDACTED" if risk_data["redactions"] > 0 else "PASSED"
            }
        }
    except ValueError as ve:
        # Handles the Pydantic validator's Security Violation
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Governance Error")