# 🛡️ Aegis — Enterprise AI Governance Gateway (Control Plane)

**Aegis** is a high-performance, security-first middleware that sits between enterprise applications and Large Language Models (LLMs).  
It acts as an **AI Governance Gate / Control Plane**, ensuring sensitive data remains protected while enforcing policy controls and producing audit-ready telemetry in real time.

---

## Why This Matters (Enterprise Context)

Uncontrolled GenAI usage introduces:

- PII and sensitive data leakage risk  
- Shadow AI adoption outside governed pathways  
- Regulatory and audit exposure  
- Unpredictable AI spend  

Aegis demonstrates how to operationalize **Zero-Trust AI** by intercepting prompts, validating policy, sanitizing content, and generating **risk + audit metadata** before any external model execution occurs.

---

## 🚀 Key Features

- **PII Shielding**  
  Uses **Microsoft Presidio** + **spaCy (NLP)** to detect and mask PII (Names, Emails, Locations, etc.)

- **Zero-Trust Policy Enforcement (Fail-Fast)**  
  **Pydantic v2** validation blocks restricted topics (e.g., Salary Data, Internal Passwords) before expensive processing occurs

- **Dynamic Risk Scoring**  
  Quantifies the risk level of each prompt, categorizing requests from `CLEAN` to `CRITICAL` based on sensitive-entity density

- **Architectural Isolation**  
  Built on **Python 3.12 (x64)** using virtual environments for stable enterprise deployment across Windows/Linux

---

## 🏗️ Technical Architecture (High Level)

Aegis follows a modular, **fail-fast governance pipeline**:

1. **Ingestion Layer**  
   FastAPI REST interface receives prompt + enterprise metadata (`user_id`, `dept`)

2. **Validation Layer**  
   Pydantic guardrails enforce policy using a `DENIED_KEYWORDS` list

3. **Governance Engine**  
   `AegisShield` runs NLP (`en_core_web_lg`) to detect and mask PII using tokens like `<PERSON>`

4. **Risk Assessment + Audit**  
   Scoring generates an audit-ready risk metric and logs governance metadata for compliance review

---

## 🧱 Technology Stack

| Component | Technology | Reason |
|--------|------------|--------|
| Language | Python 3.12.10 (x64) | Modern features with strong binary wheel stability for enterprise AI libraries |
| API Framework | FastAPI | High-performance async API + built-in Swagger docs |
| NLP Engine | spaCy 3.8.11 | Accurate Named Entity Recognition (NER) |
| Privacy Layer | Microsoft Presidio | Enterprise-grade PII detection and anonymization |
| Environment | venv + pip | Isolation to prevent dependency drift |

---

## 🛠️ Setup & Installation

Aegis is designed for **Python 3.12 (64-bit)**.

```bash
# 1. Clone & Navigate
git clone https://github.com/suresh24krishnan/aegis-governance.git
cd aegis-governance

# 2. Setup Environment
python -m venv venv_aegis
source venv_aegis/bin/activate  # Windows: .\venv_aegis\Scripts\activate

# 3. Install Requirements (Binary-Only for Stability)
pip install -r requirements.txt --only-binary :all:

# 4. Download NLP Model
python -m spacy download en_core_web_lg

# 5. Launch Gateway
fastapi dev main.py

graph TD
  subgraph Client_Layer [Client Layer]
    U((User)) -->|Prompt Request| API[FastAPI Gateway]
  end

  subgraph Governance [AI Governance Control Plane]
    API --> V{Pydantic Validator}
    V -->|Restricted Keyword| R[422 Error: Policy Violation]
    V -->|Passed| S[Aegis Shield NLP Engine]

    subgraph Privacy [Privacy Engine]
      S --> NER[spaCy Entity Recognition (NER)]
      NER --> RED[PII Redaction/Masking]
    end
  end

  subgraph Analytics [Audit & Risk]
    RED --> RS[Risk Scoring Engine]
    RS -->|Risk + Metadata| LOG[(Security Audit Log)]
  end

  RED -->|Sanitized Prompt| LLM[External LLM Provider]
  LLM -->|Response| API
  API -->|Response| U

Disclaimer

This repository is intended for architectural demonstration and portfolio purposes.

© 2026 Suresh Krishnan
