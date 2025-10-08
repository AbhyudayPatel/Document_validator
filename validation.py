"""
This contains all validation rules that are applied to extracted
insurance document data.
"""

import json
from pathlib import Path
from typing import Optional
from datetime import date
from models import ValidationResult, ExtractedData


class DocumentValidator:
    """
    Validates extracted insurance document data against business rules.
    """
    
    def __init__(self, valid_vessels_path: str = "provided_assets/valid_vessels.json"):
        """
        Initialize the validator.
        
        Args:
            valid_vessels_path: Path to the JSON file containing approved vessel names.
        """
        self.valid_vessels_path = Path(valid_vessels_path)
        self.valid_vessels = self._load_valid_vessels()
    
    def _load_valid_vessels(self) -> list[str]:
        """
        Load the list of approved vessel names from JSON file.
        
        Returns:
            List of valid vessel names.
        
        Raises:
            FileNotFoundError: If the vessels file doesn't exist.
            json.JSONDecodeError: If the file contains invalid JSON.
        """
        try:
            with open(self.valid_vessels_path, 'r', encoding='utf-8') as f:
                vessels = json.load(f)
                if not isinstance(vessels, list):
                    raise ValueError("Valid vessels file must contain a JSON array")
                return vessels
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Valid vessels file not found at: {self.valid_vessels_path}"
            )
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in vessels file: {str(e)}",
                e.doc,
                e.pos
            )
    
    def validate_date_consistency(
        self,
        start_date: Optional[date],
        end_date: Optional[date]
    ) -> ValidationResult:
        """
        Validate that the policy end date is after the start date.
        
        Args:
            start_date: Policy start date.
            end_date: Policy end date.
        
        Returns:
            ValidationResult indicating pass or fail.
        """
        rule = "Date Consistency"
        
        # Check if both dates are present
        if start_date is None or end_date is None:
            return ValidationResult(
                rule=rule,
                status="FAIL",
                message="Both start and end dates must be present for validation."
            )
        
        # Check if end date is after start date
        if end_date > start_date:
            return ValidationResult(
                rule=rule,
                status="PASS",
                message="Policy end date is after start date."
            )
        else:
            return ValidationResult(
                rule=rule,
                status="FAIL",
                message="Policy end date cannot be before the start date."
            )
    
    def validate_insured_value(self, insured_value: Optional[int]) -> ValidationResult:
        """
        Validate that the insured value is a positive number greater than zero.
        
        Args:
            insured_value: The insured value to validate.
        
        Returns:
            ValidationResult indicating pass or fail.
        """
        rule = "Value Check"
        
        if insured_value is None:
            return ValidationResult(
                rule=rule,
                status="FAIL",
                message="Insured value is missing."
            )
        
        if insured_value > 0:
            return ValidationResult(
                rule=rule,
                status="PASS",
                message="Insured value is valid."
            )
        else:
            return ValidationResult(
                rule=rule,
                status="FAIL",
                message="Insured value must be a positive number."
            )
    
    def validate_vessel_name(self, vessel_name: Optional[str]) -> ValidationResult:
        """
        Validate that the vessel name exists in the approved list.
        
        Args:
            vessel_name: The vessel name to validate.
        
        Returns:
            ValidationResult indicating pass or fail.
        """
        rule = "Vessel Name Match"
        
        if vessel_name is None or vessel_name.strip() == "":
            return ValidationResult(
                rule=rule,
                status="FAIL",
                message="Vessel name is missing."
            )
        
        if vessel_name in self.valid_vessels:
            return ValidationResult(
                rule=rule,
                status="PASS",
                message=f"Vessel '{vessel_name}' is on the approved list."
            )
        else:
            return ValidationResult(
                rule=rule,
                status="FAIL",
                message=f"Vessel '{vessel_name}' is not on the approved list."
            )
    
    def validate_policy_number(self, policy_number: Optional[str]) -> ValidationResult:
        """
        Validate that the policy number is present and not empty.
        
        Args:
            policy_number: The policy number to validate.
        
        Returns:
            ValidationResult indicating pass or fail.
        """
        rule = "Completeness Check"
        
        if policy_number is None or policy_number.strip() == "":
            return ValidationResult(
                rule=rule,
                status="FAIL",
                message="Policy number is missing."
            )
        
        return ValidationResult(
            rule=rule,
            status="PASS",
            message="Policy number is present."
        )
    
    def validate_all(self, extracted_data: ExtractedData) -> list[ValidationResult]:
        """
        Run all validation rules on the extracted data.
        
        Args:
            extracted_data: The extracted insurance document data.
        
        Returns:
            List of ValidationResult objects, one for each rule.
        """
        results = []
        
        # Run all validation rules in order
        results.append(
            self.validate_date_consistency(
                extracted_data.policy_start_date,
                extracted_data.policy_end_date
            )
        )
        
        results.append(
            self.validate_insured_value(extracted_data.insured_value)
        )
        
        results.append(
            self.validate_vessel_name(extracted_data.vessel_name)
        )
        
        results.append(
            self.validate_policy_number(extracted_data.policy_number)
        )
        
        return results
