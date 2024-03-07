from datetime import date
from dataset_definition_clinical_codes import dataset

test_data = {
    # Expected in population with matching medication
    1: {
        "patients": {"date_of_birth": date(1950, 1, 1)},
        "clinical_events": [
            {
                # First Community Pharmacy (CP) Blood Pressure (BP) Check Service
                "date": date(2022, 1, 1),
                "snomedct_code": "1659111000000107",
            },
            {
                # Second Community Pharmacy (CP) Blood Pressure (BP) Check Service
                "date": date(2022, 2, 1),
                "snomedct_code": "1659111000000107",
            },
            {
                # First Community Pharmacy (CP) Contraception Service (procedure)
                "date": date(2022, 3, 1),
                "snomedct_code": "1659121000000101",
            },
            {
                # First Community Pharmacist (CP) Consultation Service for minor illness (procedure)
                "date": date(2022, 4, 1),
                "snomedct_code": "1577041000000109",
            },
            {
                # First Pharmacy First service
                "date": date(2022, 4, 1),
                "snomedct_code": "983341000000102",
            },
            {
                # Second Pharmacy First service
                "date": date(2022, 4, 1),
                "snomedct_code": "983341000000102",
            },
            {
                # Third Pharmacy First service
                "date": date(2022, 4, 1),
                "snomedct_code": "983341000000102",
            },
        ],
        "expected_in_population": True,
        "expected_columns": {
            "count_comm_pharm_bp_service": 2,
            "count_comm_pharm_contraception_service": 1,
            "count_comm_pharm_consultation_service": 1,
            "count_pharm_first_service": 3,
        },
    },
}
