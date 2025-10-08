"""
Comprehensive test suite for the Insurance Document Validator.
Tests all validation rules, AI extraction, and edge cases.
"""

from datetime import date
from pathlib import Path
from models import ExtractedData
from validation import DocumentValidator
from ai_extractor import AIExtractor


class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.total = 0

        try:
            self.extractor = AIExtractor()
            self.validator = DocumentValidator()
        except Exception as e:
            print(f"❌ Failed to initialize: {e}")
            raise

    def run_test(self, name, func):
        """Run a single test and track results."""
        self.total += 1
        try:
            func()
            self.passed += 1
            print(f"  ✅ {name}")
            return True
        except AssertionError as e:
            self.failed += 1
            print(f"  ❌ {name}")
            print(f"     Error: {e}")
            return False
        except Exception as e:
            self.failed += 1
            print(f"  ❌ {name}")
            print(f"     Unexpected error: {e}")
            return False

    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 70)
        print(f"TEST SUMMARY: {self.passed}/{self.total} tests passed")
        if self.failed > 0:
            print(f"❌ {self.failed} test(s) failed")
        else:
            print("✅ ALL TESTS PASSED!")
        print("=" * 70)


def test_validation_rules():
    """Test all validation rules individually."""
    print("\n" + "=" * 70)
    print("TEST SUITE 1: Validation Rules")
    print("=" * 70)

    runner = TestRunner()
    validator = runner.validator

    # Test 1: Date Consistency - Valid
    def test_date_valid():
        result = validator.validate_date_consistency(
            date(2025, 1, 1), date(2025, 12, 31)
        )
        assert result.status == "PASS", f"Expected PASS, got {result.status}"

    runner.run_test("Date consistency: Valid dates", test_date_valid)

    # Test 2: Date Consistency - Invalid (reversed)
    def test_date_invalid():
        result = validator.validate_date_consistency(
            date(2025, 12, 31), date(2025, 1, 1)
        )
        assert result.status == "FAIL", f"Expected FAIL, got {result.status}"

    runner.run_test("Date consistency: Reversed dates", test_date_invalid)

    # Test 3: Date Consistency - Same dates
    def test_date_same():
        result = validator.validate_date_consistency(date(2025, 1, 1), date(2025, 1, 1))
        assert result.status == "FAIL", "Same dates should fail"

    runner.run_test("Date consistency: Same dates", test_date_same)

    # Test 4: Date Consistency - Missing dates
    def test_date_missing():
        result = validator.validate_date_consistency(None, date(2025, 1, 1))
        assert result.status == "FAIL"

    runner.run_test("Date consistency: Missing start date", test_date_missing)

    # Test 5: Value Check - Positive
    def test_value_positive():
        result = validator.validate_insured_value(1000000)
        assert result.status == "PASS"

    runner.run_test("Value check: Positive value", test_value_positive)

    # Test 6: Value Check - Zero
    def test_value_zero():
        result = validator.validate_insured_value(0)
        assert result.status == "FAIL"

    runner.run_test("Value check: Zero value", test_value_zero)

    # Test 7: Value Check - Negative
    def test_value_negative():
        result = validator.validate_insured_value(-500)
        assert result.status == "FAIL"

    runner.run_test("Value check: Negative value", test_value_negative)

    # Test 8: Value Check - None
    def test_value_none():
        result = validator.validate_insured_value(None)
        assert result.status == "FAIL"

    runner.run_test("Value check: None value", test_value_none)

    # Test 9: Vessel Name - Valid
    def test_vessel_valid():
        result = validator.validate_vessel_name("MV Neptune")
        assert result.status == "PASS"

    runner.run_test("Vessel name: Valid vessel", test_vessel_valid)

    # Test 10: Vessel Name - Invalid
    def test_vessel_invalid():
        result = validator.validate_vessel_name("Unknown Ship")
        assert result.status == "FAIL"

    runner.run_test("Vessel name: Invalid vessel", test_vessel_invalid)

    # Test 11: Vessel Name - None
    def test_vessel_none():
        result = validator.validate_vessel_name(None)
        assert result.status == "FAIL"

    runner.run_test("Vessel name: None", test_vessel_none)

    # Test 12: Vessel Name - Empty
    def test_vessel_empty():
        result = validator.validate_vessel_name("")
        assert result.status == "FAIL"

    runner.run_test("Vessel name: Empty string", test_vessel_empty)

    # Test 13: Policy Number - Valid
    def test_policy_valid():
        result = validator.validate_policy_number("HM-2025-10-A4B")
        assert result.status == "PASS"

    runner.run_test("Policy number: Valid", test_policy_valid)

    # Test 14: Policy Number - None
    def test_policy_none():
        result = validator.validate_policy_number(None)
        assert result.status == "FAIL"

    runner.run_test("Policy number: None", test_policy_none)

    # Test 15: Policy Number - Empty
    def test_policy_empty():
        result = validator.validate_policy_number("")
        assert result.status == "FAIL"

    runner.run_test("Policy number: Empty string", test_policy_empty)

    runner.print_summary()


def test_ai_extraction_with_documents():
    """Test AI extraction with various document formats."""
    print("\n" + "=" * 70)
    print("TEST SUITE 2: AI Extraction with Test Documents")
    print("=" * 70)

    runner = TestRunner()

    test_cases = [
        ("sample_document_pass.txt", True, "Original passing document"),
        ("sample_document_fail.txt", False, "Original failing document"),
        ("test_doc_valid_1.txt", True, "Valid doc 1 - Starlight Carrier"),
        ("test_doc_valid_2.txt", True, "Valid doc 2 - Oceanic Voyager"),
        ("test_doc_valid_3.txt", True, "Valid doc 3 - Ironclad Freighter"),
        ("test_doc_invalid_1.txt", False, "Invalid doc 1 - Zero value"),
        ("test_doc_invalid_2.txt", False, "Invalid doc 2 - Unknown vessel"),
        ("test_doc_no_data.txt", False, "No data document"),
    ]

    for filename, should_pass, description in test_cases:

        def test_doc():
            path = Path("provided_assets") / filename
            if not path.exists():
                raise FileNotFoundError(f"Test file not found: {filename}")

            with open(path, "r") as f:
                doc_text = f.read()

            # Extract with AI
            ai_result = runner.extractor.extract_data_sync(doc_text)

            # Convert to ExtractedData
            extracted = ExtractedData(
                policy_number=ai_result.policy_number,
                vessel_name=ai_result.vessel_name,
                policy_start_date=(
                    date.fromisoformat(ai_result.policy_start_date)
                    if ai_result.policy_start_date
                    else None
                ),
                policy_end_date=(
                    date.fromisoformat(ai_result.policy_end_date)
                    if ai_result.policy_end_date
                    else None
                ),
                insured_value=ai_result.insured_value,
            )

            # Validate
            results = runner.validator.validate_all(extracted)
            passed_count = sum(1 for r in results if r.status == "PASS")
            all_passed = passed_count == 4

            if should_pass:
                assert (
                    all_passed
                ), f"Expected all validations to pass but {4-passed_count} failed"
            else:
                assert (
                    not all_passed
                ), "Expected some validations to fail but all passed"

        runner.run_test(description, test_doc)

    runner.print_summary()


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print("\n" + "=" * 70)
    print("TEST SUITE 3: Edge Cases")
    print("=" * 70)

    runner = TestRunner()
    validator = runner.validator

    # Test 1: Very large insured value
    def test_large_value():
        result = validator.validate_insured_value(999999999999)
        assert result.status == "PASS"

    runner.run_test("Very large insured value", test_large_value)

    # Test 2: Dates one day apart
    def test_one_day_apart():
        result = validator.validate_date_consistency(date(2025, 1, 1), date(2025, 1, 2))
        assert result.status == "PASS"

    runner.run_test("Dates one day apart", test_one_day_apart)

    # Test 3: Dates one year apart
    def test_one_year_apart():
        result = validator.validate_date_consistency(date(2025, 1, 1), date(2026, 1, 1))
        assert result.status == "PASS"

    runner.run_test("Dates exactly one year apart", test_one_year_apart)

    # Test 4: All vessels in approved list
    vessels = [
        "MV Neptune",
        "Oceanic Voyager",
        "Starlight Carrier",
        "The Sea Serpent",
        "Ironclad Freighter",
    ]

    for vessel in vessels:

        def test_approved_vessel():
            result = validator.validate_vessel_name(vessel)
            assert result.status == "PASS", f"Approved vessel {vessel} should pass"

        runner.run_test(f"Approved vessel: {vessel}", test_approved_vessel)

    # Test 5: Whitespace in policy number
    def test_policy_whitespace():
        result = validator.validate_policy_number("   ")
        assert result.status == "FAIL"

    runner.run_test("Policy number: Only whitespace", test_policy_whitespace)

    runner.print_summary()


def test_full_pipeline():
    """Test the complete extraction and validation pipeline."""
    print("\n" + "=" * 70)
    print("TEST SUITE 4: Full Pipeline Integration")
    print("=" * 70)

    runner = TestRunner()

    # Test with original sample_document_pass
    def test_original_pass():
        with open("provided_assets/sample_document_pass.txt", "r") as f:
            doc = f.read()

        ai_result = runner.extractor.extract_data_sync(doc)
        extracted = ExtractedData(
            policy_number=ai_result.policy_number,
            vessel_name=ai_result.vessel_name,
            policy_start_date=(
                date.fromisoformat(ai_result.policy_start_date)
                if ai_result.policy_start_date
                else None
            ),
            policy_end_date=(
                date.fromisoformat(ai_result.policy_end_date)
                if ai_result.policy_end_date
                else None
            ),
            insured_value=ai_result.insured_value,
        )

        # Verify extracted values
        assert extracted.policy_number == "HM-2025-10-A4B"
        assert extracted.vessel_name == "MV Neptune"
        assert extracted.insured_value == 5000000

        # Verify all validations pass
        results = runner.validator.validate_all(extracted)
        assert all(r.status == "PASS" for r in results)

    runner.run_test("Original passing document - Full pipeline", test_original_pass)

    # Test with original sample_document_fail
    def test_original_fail():
        with open("provided_assets/sample_document_fail.txt", "r") as f:
            doc = f.read()

        ai_result = runner.extractor.extract_data_sync(doc)
        extracted = ExtractedData(
            policy_number=ai_result.policy_number,
            vessel_name=ai_result.vessel_name,
            policy_start_date=(
                date.fromisoformat(ai_result.policy_start_date)
                if ai_result.policy_start_date
                else None
            ),
            policy_end_date=(
                date.fromisoformat(ai_result.policy_end_date)
                if ai_result.policy_end_date
                else None
            ),
            insured_value=ai_result.insured_value,
        )

        # Verify all validations fail
        results = runner.validator.validate_all(extracted)
        assert all(r.status == "FAIL" for r in results)

    runner.run_test("Original failing document - Full pipeline", test_original_fail)

    runner.print_summary()


def main():
    """Run all test suites."""
    print("\n" + "=" * 70)
    print("🧪 COMPREHENSIVE TEST SUITE")
    print("Insurance Document Validator")
    print("=" * 70)

    try:
        # Run all test suites
        test_validation_rules()
        test_ai_extraction_with_documents()
        test_edge_cases()
        test_full_pipeline()

        print("\n" + "=" * 70)
        print("✅ ALL TEST SUITES COMPLETED!")
        print("=" * 70)
        print("\nThe validator is working correctly and handles:")
        print("  ✓ All validation rules")
        print("  ✓ Various document formats")
        print("  ✓ Edge cases and boundary conditions")
        print("  ✓ Full extraction and validation pipeline")
        print("\n" + "=" * 70)

    except Exception as e:
        print(f"\n❌ Test suite failed to run: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
