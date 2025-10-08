# 🚢 Mini Insurance Document Validator

A FastAPI-powered microservice that validates insurance documents using AI-powered data extraction and business rule validation.

## 📋 Overview

This application automatically validates insurance documents by:
1. **Extracting** structured data from unstructured document text using Google's Gemini AI
2. **Validating** the extracted data against business rules
3. **Returning** detailed validation results via a RESTful API

## 🎯 Features

- **AI-Powered Extraction**: Uses Google Gemini 2.0 Flash for intelligent document parsing
- **Structured Output**: Leverages Pydantic models for type-safe data validation
- **Business Rules Validation**:
  - ✅ Date consistency checks
  - ✅ Value validation (positive numbers)
  - ✅ Vessel name verification against approved list
  - ✅ Completeness checks for required fields
- **Clean Architecture**: Modular design with separated concerns
- **Type-Safe**: Full type hints throughout the codebase
- **Production-Ready**: Comprehensive error handling and logging

## 🏗️ Project Structure

```
genoshi/
├── main.py                  # FastAPI application entry point
├── models.py                # Pydantic data models
├── ai_extractor.py         # AI extraction service (Gemini integration)
├── validation.py           # Business validation logic
├── pyproject.toml          # Project dependencies
├── .env                    # Environment variables (API keys)
├── README.md               # This file
└── provided_assets/
    ├── sample_document_pass.txt    # Sample document (should pass)
    ├── sample_document_fail.txt    # Sample document (should fail)
    └── valid_vessels.json          # Approved vessel names
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- A Google Gemini API key ([Get one here](https://ai.google.dev/))

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd genoshi
   ```

2. **Set up your environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   GEMINI_API_KEY=your_actual_api_key_here
   ```
   
   Or set it as an environment variable:
   ```bash
   # Windows (PowerShell)
   $env:GEMINI_API_KEY = "your_actual_api_key_here"
   
   # Windows (CMD)
   setx GEMINI_API_KEY "your_actual_api_key_here"
   
   # Linux/Mac
   export GEMINI_API_KEY="your_actual_api_key_here"
   ```

3. **Install dependencies**
   
   Using `uv` (recommended):
   ```bash
   uv sync
   ```
   
   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the FastAPI server:

```bash
# Using uv
uv run uvicorn main:app --reload

# Or with uvicorn directly
uvicorn main:app --reload
```

The API will be available at: **http://localhost:8000**

### API Documentation

Once running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📡 API Usage

### Endpoint: `POST /validate`

Validates an insurance document by extracting and validating its data.

#### Request Body

```json
{
  "document_text": "*** OFFICIAL COVER NOTE ***\nPolicy HM-2025-10-A4B for MV Neptune..."
}
```

#### Response (Success Example)

```json
{
  "extracted_data": {
    "policy_number": "HM-2025-10-A4B",
    "vessel_name": "MV Neptune",
    "policy_start_date": "2025-11-01",
    "policy_end_date": "2026-10-31",
    "insured_value": 5000000
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
      "message": "Vessel 'MV Neptune' is on the approved list."
    },
    {
      "rule": "Completeness Check",
      "status": "PASS",
      "message": "Policy number is present."
    }
  ]
}
```

#### Response (Failure Example)

```json
{
  "extracted_data": {
    "policy_number": null,
    "vessel_name": "The Wanderer",
    "policy_start_date": "2026-01-01",
    "policy_end_date": "2025-12-31",
    "insured_value": -500
  },
  "validation_results": [
    {
      "rule": "Date Consistency",
      "status": "FAIL",
      "message": "Policy end date cannot be before the start date."
    },
    {
      "rule": "Value Check",
      "status": "FAIL",
      "message": "Insured value must be a positive number."
    },
    {
      "rule": "Vessel Name Match",
      "status": "FAIL",
      "message": "Vessel 'The Wanderer' is not on the approved list."
    },
    {
      "rule": "Completeness Check",
      "status": "FAIL",
      "message": "Policy number is missing."
    }
  ]
}
```

## 🧪 Testing

### Quick Test (Without Starting Server)

Run the included test script to verify everything works:

```bash
# Test the core logic and AI extraction
uv run python test.py
```

This will test:
- ✅ Validation logic with both valid and invalid data
- ✅ AI extraction with both sample documents
- ✅ Full pipeline (extraction + validation)

### API Testing

1. **Start the server:**
   ```bash
   uv run uvicorn main:app --reload
   ```

2. **Test via Swagger UI:**
   - Open http://localhost:8000/docs
   - Click on the `/validate` endpoint
   - Click "Try it out"
   - Copy the content from `provided_assets/sample_document_pass.txt`
   - Paste it into the `document_text` field (keep it as a single line or use proper JSON escaping)
   - Click "Execute"

3. **Test via curl (PowerShell):**
   ```powershell
   $doc = Get-Content "provided_assets/sample_document_pass.txt" -Raw
   $body = @{ document_text = $doc } | ConvertTo-Json
   Invoke-RestMethod -Uri "http://localhost:8000/validate" -Method Post -Body $body -ContentType "application/json"
   ```

## 🏛️ Architecture

### Modular Design

The application follows clean architecture principles with clear separation of concerns:

1. **`models.py`**: Data models and schemas (Pydantic)
2. **`ai_extractor.py`**: AI integration layer (Gemini API)
3. **`validation.py`**: Business logic and validation rules
4. **`main.py`**: API routes and application setup (FastAPI)

### AI Extraction Strategy

The AI extraction uses:
- **Model**: Google Gemini 2.0 Flash (fast and cost-effective)
- **Technique**: Structured output with Pydantic schema enforcement
- **Prompt Engineering**: Detailed instructions for accurate field extraction
- **Error Handling**: Graceful degradation with informative error messages

### Validation Rules

| Rule | Description | Pass Criteria |
|------|-------------|---------------|
| **Date Consistency** | Validates date logic | End date > Start date |
| **Value Check** | Validates insured amount | Value > 0 |
| **Vessel Name Match** | Checks against approved list | Name in `valid_vessels.json` |
| **Completeness Check** | Ensures required fields | Policy number not null/empty |

## 🔐 Security

- ✅ API keys managed via environment variables
- ✅ No hardcoded secrets
- ✅ `.env` file excluded from version control
- ✅ Input validation with Pydantic
- ✅ Error messages don't leak sensitive information

## 🛠️ Technology Stack

- **Framework**: FastAPI 0.118.1
- **AI Model**: Google Gemini 2.0 Flash
- **Data Validation**: Pydantic v2
- **HTTP Server**: Uvicorn
- **Package Management**: uv
- **Python Version**: 3.12+

## 📝 Development Notes

### Adding New Validation Rules

To add a new validation rule:

1. Add a method to `DocumentValidator` in `validation.py`
2. Call it in the `validate_all()` method
3. Return a `ValidationResult` with rule name, status, and message

### Modifying AI Extraction

To adjust the AI extraction:

1. Edit the `EXTRACTION_PROMPT` in `ai_extractor.py`
2. Modify the `AIExtractedData` schema if adding/removing fields
3. Update the `ExtractedData` model in `models.py` accordingly

## 🐛 Troubleshooting

### "AI service not available" Error
- Ensure `GEMINI_API_KEY` is set correctly
- Check that the API key is valid and has quota
- Verify internet connection

### "Valid vessels file not found" Error
- Ensure `provided_assets/valid_vessels.json` exists
- Check file permissions

### Date Parsing Issues
- The AI should return dates in ISO format (YYYY-MM-DD)
- If issues persist, check the AI extraction prompt

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Google Gemini API](https://ai.google.dev/)
- [Gemini API Python SDK](https://github.com/google/generative-ai-python)

## 📄 License

This project is part of a technical assessment for Genoshi.

## 👥 Author

Built as part of the Genoshi Backend Challenge.

---

**Happy Validating! 🎉**
