"""
Pydantic models for the Insurance Document Validator API.

This module defines all data models used for request/response validation
and data extraction.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class DocumentRequest(BaseModel):
    """Request model for the document text."""

    document_text: str = Field(
        ..., description="The raw text content of the insurance document.", min_length=1
    )


class ExtractedData(BaseModel):
    """
    Model for the data extracted by the AI service from insurance documents.

    This represents the structured information that the AI extracts from
    unstructured document text.
    """

    policy_number: Optional[str] = Field(
        None, description="The unique policy reference number"
    )
    vessel_name: Optional[str] = Field(
        None, description="The name of the insured vessel"
    )
    policy_start_date: Optional[date] = Field(
        None, description="The effective start date of the policy"
    )
    policy_end_date: Optional[date] = Field(
        None, description="The expiration date of the policy"
    )
    insured_value: Optional[int] = Field(
        None, description="The total insured value in USD (as integer)"
    )


class ValidationResult(BaseModel):
    """Model for a single validation check result."""

    rule: str = Field(..., description="The name of the validation rule being checked")
    status: str = Field(
        ..., description="The status of the validation: 'PASS' or 'FAIL'"
    )
    message: str = Field(
        ..., description="A human-readable message explaining the result"
    )


class ValidationResponse(BaseModel):
    """The final response model for the /validate endpoint."""

    extracted_data: ExtractedData = Field(
        ..., description="The structured data extracted from the document"
    )
    validation_results: list[ValidationResult] = Field(
        ..., description="List of validation check results"
    )
