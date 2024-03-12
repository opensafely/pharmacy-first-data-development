from datetime import date
from analysis.dataset_definition_curation import dataset

test_data = {
    # Expected in population with matching medication
    1: {
        "patients": {"date_of_birth": date(1950, 1, 1)},
        "medications_raw": [
            {
                # First before Pharmacy first launch
                "date": date(2024, 1, 1),
                "dmd_code": "39113611000001102",
                "medication_status": 1,
            },
            {
                # Last before Pharmacy first launch (same code)
                "date": date(2024, 1, 30),
                "dmd_code": "39113611000001102",
                "medication_status": 1,
            },
            {
                # First after Pharmacy first launch
                "date": date(2024, 1, 31),
                "dmd_code": "39113611000001107",
                "medication_status": 3,
            },
        ],
        "expected_in_population": True,
        "expected_columns": {
            "pre_first_dmd_code": "39113611000001102",
            "post_first_dmd_code": "39113611000001107",
            "pre_first_medication_status": 1,
            "post_first_medication_status": 3,
        },
    },
    2: {
        "patients": {"date_of_birth": date(1950, 1, 1)},
        "medications_raw": [
            {
                # First after Pharmacy first launch
                "date": date(2024, 3, 1),
                "dmd_code": "39113611000001102",
                "medication_status": 11,
            },
            {
                # Second after Pharmacy first launch (different code)
                "date": date(2024, 3, 1),
                "dmd_code": "39113611000001107",
                "medication_status": 12,
            },
        ],
        "expected_in_population": True,
        "expected_columns": {
            "pre_first_dmd_code": None,
            "post_first_dmd_code": "39113611000001102",
            "pre_first_medication_status": None,
            "post_first_medication_status": 11,
        },
    },
}
