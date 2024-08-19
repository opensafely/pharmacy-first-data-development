from datetime import date
from analysis.dataset_definition_pf_data_development import dataset

# Run the following command in the terminal to test the dataset definition dataset_definition_pf_data_development
# opensafely exec ehrql:v1 assure analysis/test_dataset_definition_pf_data_development.py
test_data = {
    # Expected in population with matching medication
    1: {
        "patients": {"date_of_birth": date(1950, 1, 1)},
        "clinical_events": [
            {
                # Community Pharmacy (CP) Blood Pressure (BP) Check Service
                # First before launch
                "consultation_id": 1,
                "date": date(2024, 1, 1),
                "snomedct_code": "1659111000000107",
            },
            {
                # Community Pharmacy (CP) Blood Pressure (BP) Check Service
                # First after launch
                "consultation_id": 2,
                "date": date(2024, 2, 1),
                "snomedct_code": "1659111000000107",
            },
        ],
        "medications_raw": [
            {
                # First before Pharmacy first launch
                # consultation_id not linked to pharmacy first code in clinical_events
                "consultation_id": 3,
                "date": date(2024, 1, 1),
                "dmd_code": "20129711000001103",
                "medication_status": 3,
            },
            {
                # Last before Pharmacy first launch (same code)
                "consultation_id": 1,
                "date": date(2024, 1, 2),
                "dmd_code": "37772611000001104",
                "medication_status": 1,
            },
            {
                # First after Pharmacy first launch
                # But not a dmd code from the PF codelists
                "consultation_id": 2,
                "date": date(2024, 2, 1),
                "dmd_code": "10010100",
                "medication_status": 4,
            },
            {
                # Second after Pharmacy first launch
                "consultation_id": 2,
                "date": date(2024, 2, 2),
                "dmd_code": "78111000001109",
                "medication_status": 3,
            },
        ],
        "expected_in_population": True,
        "expected_columns": {
            "pre_first_dmd_code": "37772611000001104",
            "post_first_dmd_code": "78111000001109",
            "pre_first_medication_status": 1,
            "post_first_medication_status": 3,
        },
    },
    2: {
        "patients": {"date_of_birth": date(1950, 1, 1)},
        "clinical_events": [
            {
                # Community Pharmacy (CP) Blood Pressure (BP) Check Service
                # First before launch
                "consultation_id": 1,
                "date": date(2024, 1, 1),
                "snomedct_code": "1659111000000107",
            },
            {
                # Community Pharmacy (CP) Blood Pressure (BP) Check Service
                # First after launch
                "consultation_id": 1,
                "date": date(2024, 2, 1),
                "snomedct_code": "1659111000000107",
            },
        ],
        "medications_raw": [
            {
                # First after Pharmacy first launch
                "consultation_id": 1,
                "date": date(2024, 3, 1),
                "dmd_code": "21532411000001101",
                "medication_status": 11,
            },
            {
                # Second after Pharmacy first launch (different code)
                "consultation_id": 1,
                "date": date(2024, 3, 2),
                "dmd_code": "10381311000001104",
                "medication_status": 12,
            },
        ],
        "expected_in_population": True,
        "expected_columns": {
            "pre_first_dmd_code": None,
            "post_first_dmd_code": "21532411000001101",
            "pre_first_medication_status": None,
            "post_first_medication_status": 11,
        },
    },
    # Expected in population with matching medication
    3: {
        "patients": {"date_of_birth": date(1950, 1, 1)},
        "clinical_events": [
            {
                # Community Pharmacy (CP) Blood Pressure (BP) Check Service
                # First before launch
                "consultation_id": 1,
                "date": date(2024, 1, 1),
                "snomedct_code": "1659111000000107",
            },
            {
                # Community Pharmacy (CP) Blood Pressure (BP) Check Service
                # First after launch
                "consultation_id": 1,
                "date": date(2024, 2, 1),
                "snomedct_code": "1659111000000107",
            },
            {
                # Community Pharmacy (CP) Contraception Service (procedure)
                # First after launch
                "consultation_id": 1,
                "date": date(2024, 3, 1),
                "snomedct_code": "1659121000000101",
            },
            {
                # Community Pharmacist (CP) Consultation Service for minor illness (procedure)
                # First after launch
                "consultation_id": 1,
                "date": date(2024, 4, 1),
                "snomedct_code": "1577041000000109",
            },
            {
                # Pharmacy First service
                # First before launch
                "consultation_id": 1,
                "date": date(2023, 12, 1),
                "snomedct_code": "983341000000102",
            },
            {
                # Pharmacy First service
                # First after launch
                "consultation_id": 1,
                "date": date(2024, 4, 1),
                "snomedct_code": "983341000000102",
            },
            {
                # Pharmacy First service
                # Second after launch, same day
                "consultation_id": 1,
                "date": date(2024, 4, 1),
                "snomedct_code": "983341000000102",
            },
            {
                # Third Pharmacy First service
                # Third after launch, different day
                "consultation_id": 1,
                "date": date(2024, 4, 2),
                "snomedct_code": "983341000000102",
            },
        ],
        "medications_raw": [],
        "expected_in_population": True,
        "expected_columns": {
            "pre_count_comm_pharm_bp_service": 1,
            "pre_count_comm_pharm_contraception_service": 0,
            "pre_count_comm_pharm_consultation_service": 0,
            "pre_count_pharm_first_service": 1,
            "post_count_comm_pharm_bp_service": 1,
            "post_count_comm_pharm_contraception_service": 1,
            "post_count_comm_pharm_consultation_service": 1,
            "post_count_pharm_first_service": 3,
        },
    },
}
