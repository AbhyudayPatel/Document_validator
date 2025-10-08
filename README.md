# 🚢 Mini Insurance Document Validator

A FastAPI microservice that validates insurance documents 
## 🎯 Features

- **AI-Powered Extraction**: Extracts structured data from unstructured documents using Gemini 2.0 Flash
- **Business Validation**: Date consistency, value checks, vessel verification, and completeness validation
- **Clean Architecture**: Modular design with separated concerns
- **Type-Safe**: Pydantic models throughout

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Google Gemini API key

### Installation

```bash
# Clone and navigate
git clone https://github.com/AbhyudayPatel/Document_validator.git
cd Document_validator

# Set up environment variable
$env:GEMINI_API_KEY = "your_actual_api_key_here"

# Install dependencies
uv sync

# Run the server
uv run uvicorn main:app --reload
```

**API Available at:** http://localhost:8000  
**API Docs:** http://localhost:8000/docs

## 📡 API Usage

### `POST /validate`

**Request:**
```json
{
  "document_text": "MARINE INSURANCE CERTIFICATE Certificate No: MIC-2025-STAR-789 Vessel Information: This certificate is issued for the vessel 'Starlight Carrier' Insurance Period: Commencement: January 15, 2025 Termination: 14-01-2026 Coverage Amount: The sum insured under this policy is Ten Million US Dollars ($10,000,000) This certificate is valid and binding upon the issuance date"
}
```

**Response:**
```json
{
  "extracted_data": {
    "policy_number": "MIC-2025-STAR-789",
    "vessel_name": "Starlight Carrier",
    "policy_start_date": "2025-01-15",
    "policy_end_date": "2026-01-14",
    "insured_value": 10000000
  },
  "validation_results": [
    {
      "rule": "Date Consistency",
      "status": "PASS",
      "message": "Policy end date is after start date."
    },
    {
      "rule": "Value Check",
      "status": "PASS",
      "message": "Insured value is valid."
    },
    {
      "rule": "Vessel Name Match",
      "status": "PASS",
      "message": "Vessel 'Starlight Carrier' is on the approved list."
    },
    {
      "rule": "Completeness Check",
      "status": "PASS",
      "message": "Policy number is present."
    }
  ]
}
```

## 🧪 Testing

```bash
# Test via included test script
uv run python test_comprehensive.py

# Test via PowerShell
$doc = Get-Content "provided_assets/sample_document_pass.txt" -Raw
$body = @{ document_text = $doc } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/validate" -Method Post -Body $body -ContentType "application/json"
```

## �️ Architecture

**Modular Design:**
- `main.py` - FastAPI application and routes
- `models.py` - Pydantic data models
- `ai_extractor.py` - Gemini AI integration
- `validation.py` - Business validation logic

**Validation Rules:**
- Date Consistency (end date > start date)
- Value Check (insured value > 0)
- Vessel Name Match (against approved list)
- Completeness Check (required fields present)

## 🛠️ Technology Stack

- FastAPI 0.118.1
- Google Gemini 2.0 Flash
- Pydantic v2
- Uvicorn
- Python 3.12+

##  Troubleshooting

- **"AI service not available"**: Verify `GEMINI_API_KEY` is set and valid
- **"Valid vessels file not found"**: Ensure `provided_assets/valid_vessels.json` exists
- **Date parsing issues**: AI returns dates in ISO format (YYYY-MM-DD)

---

This project demonstrates my ability to architect a full application and leverage modern AI tools like Copilot to accelerate development. The core logic, database schema, and system design are my own, while AI was used for boilerplate and test generation, reflecting a real-world development workflow.
