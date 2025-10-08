"""
Mini Insurance Document Validator - FastAPI Application

This application provides an API endpoint to validate insurance documents
by extracting structured data using AI and applying business validation rules.
"""

from fastapi import FastAPI, HTTPException
from datetime import date

from dotenv import load_dotenv
load_dotenv()

# Import our modular components
from models import DocumentRequest, ExtractedData, ValidationResponse
from ai_extractor import AIExtractor
from validation import DocumentValidator


# --- FastAPI Application Setup ---
app = FastAPI(
    title="Mini Insurance Document Validator",
    description="An API to validate insurance documents using AI extraction and business rules.",
    version="1.0.0"
)

# --- Initialize Services ---
# These are initialized once at startup for efficiency
try:
    ai_extractor = AIExtractor()
    document_validator = DocumentValidator()
except ValueError as e:
    print(f"⚠️  WARNING: {str(e)}")
    print("The API will not function without a valid GEMINI_API_KEY.")
    ai_extractor = None
    document_validator = None
except FileNotFoundError as e:
    print(f"⚠️  WARNING: {str(e)}")
    document_validator = None


# --- API Endpoints ---

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "Mini Insurance Document Validator",
        "status": "running",
        "version": "1.0.0"
    }


@app.post("/validate", response_model=ValidationResponse)
async def validate_document(request: DocumentRequest):
    """
    Validates an insurance document by extracting data via AI and running business rules.
    
    This endpoint:
    1. Extracts structured data from the document text using Gemini AI
    2. Validates the extracted data against business rules:
       - Date Consistency: End date must be after start date
       - Value Check: Insured value must be positive
       - Vessel Name Match: Vessel must be on approved list
       - Completeness Check: Policy number must be present
    
    Args:
        request: DocumentRequest containing the raw document text
    
    Returns:
        ValidationResponse with extracted data and validation results
    
    Raises:
        HTTPException: If AI service fails or validation cannot be performed
    """
    # Check if services are initialized
    if ai_extractor is None:
        raise HTTPException(
            status_code=503,
            detail="AI service not available. Please configure GEMINI_API_KEY."
        )
    
    if document_validator is None:
        raise HTTPException(
            status_code=503,
            detail="Validation service not available. Check valid_vessels.json file."
        )
    
    # Step 1: Extract data from document using AI
    try:
        ai_extracted = ai_extractor.extract_data_sync(request.document_text)
        
        # Convert AI extracted data to our response model
        # Parse dates if they exist
        start_date = None
        end_date = None
        
        if ai_extracted.policy_start_date:
            try:
                start_date = date.fromisoformat(ai_extracted.policy_start_date)
            except (ValueError, TypeError):
                pass  # Will be handled in validation
        
        if ai_extracted.policy_end_date:
            try:
                end_date = date.fromisoformat(ai_extracted.policy_end_date)
            except (ValueError, TypeError):
                pass  # Will be handled in validation
        
        extracted_data = ExtractedData(
            policy_number=ai_extracted.policy_number,
            vessel_name=ai_extracted.vessel_name,
            policy_start_date=start_date,
            policy_end_date=end_date,
            insured_value=ai_extracted.insured_value
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI extraction failed: {str(e)}"
        )
    
    # Step 2: Validate the extracted data
    try:
        validation_results = document_validator.validate_all(extracted_data)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Validation failed: {str(e)}"
        )
    
    # Step 3: Return the complete response
    return ValidationResponse(
        extracted_data=extracted_data,
        validation_results=validation_results
    )