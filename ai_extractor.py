"""
llm extraction service for insurance documents.
"""

import os
from typing import Optional
from google import genai
from pydantic import BaseModel, Field


class AIExtractedData(BaseModel):

    policy_number: Optional[str] = Field(
        None, description="The policy reference number or ID (e.g., 'HM-2025-10-A4B')"
    )
    vessel_name: Optional[str] = Field(
        None, description="The name of the vessel being insured"
    )
    policy_start_date: Optional[str] = Field(
        None, description="Policy start/effective date in ISO format YYYY-MM-DD"
    )
    policy_end_date: Optional[str] = Field(
        None, description="Policy end/expiration date in ISO format YYYY-MM-DD"
    )
    insured_value: Optional[int] = Field(
        None,
        description="Total insured value as an integer (no currency symbols or decimals)",
    )


class AIExtractor:

    EXTRACTION_PROMPT = """You are an expert insurance document parser. Your task is to carefully read the provided insurance document text and extract the following key information:

1. **policy_number**: The unique policy reference number or ID. Look for terms like "policy number", "reference number", "policy ID", etc. If not found or explicitly stated as missing/blank/pending, return null.

2. **vessel_name**: The name of the vessel/ship being insured. Look for phrases like "vessel named", "vessel:", "ship:", etc. Return the exact name found.

3. **policy_start_date**: The policy effective/start date. This may be written in various formats like "November 1st, 2025", "Jan 1, 2026", "2025-11-01", etc. Convert it to ISO format (YYYY-MM-DD).

4. **policy_end_date**: The policy expiration/end date. Convert to ISO format (YYYY-MM-DD).

5. **insured_value**: The total insured value. This may appear as "$5,000,000 USD", "5 million dollars", etc. Extract only the numeric value as an integer (e.g., 5000000). Include negative values if present (e.g., -500).

**Important Instructions:**
- If any field is not found in the document, explicitly stated as missing, blank, or pending, return null for that field.
- For dates, convert all formats to ISO format (YYYY-MM-DD).
- For insured_value, remove all currency symbols, commas, and text. Return only the integer value.
- Be careful with negative values - if the document mentions a debit or negative amount, include the minus sign.
- Extract information exactly as it appears, don't make assumptions.

**Document to parse:**
{document_text}

Extract the information and return it as structured JSON."""

    def __init__(self, api_key: Optional[str] = None):

        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Please set GEMINI_API_KEY environment variable."
            )

        self.client = genai.Client(api_key=self.api_key)

    async def extract_data(self, document_text: str) -> AIExtractedData:

        try:
            # Format the prompt with the document text
            prompt = self.EXTRACTION_PROMPT.format(document_text=document_text)

            # Call Gemini with structured output (JSON mode)
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": AIExtractedData,
                },
            )

            # Use the parsed response (Gemini automatically validates against schema)
            extracted: AIExtractedData = response.parsed

            return extracted

        except Exception as e:
            raise Exception(f"AI extraction failed: {str(e)}") from e

    def extract_data_sync(self, document_text: str) -> AIExtractedData:
        """
        Synchronous version of extract_data for non-async contexts.

        Args:
            document_text: The raw text content of the insurance document.

        Returns:
            AIExtractedData: Structured data extracted from the document.

        Raises:
            Exception: If the AI service fails or returns invalid data.
        """
        try:
            prompt = self.EXTRACTION_PROMPT.format(document_text=document_text)

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": AIExtractedData,
                },
            )

            extracted: AIExtractedData = response.parsed
            return extracted

        except Exception as e:
            raise Exception(f"AI extraction failed: {str(e)}") from e
