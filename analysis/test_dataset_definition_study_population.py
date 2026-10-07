from datetime import date
from analysis.dataset_definition_study_population import dataset

# Run the following command in the terminal to test the dataset definition dataset_definition_study_population
# opensafely exec ehrql:v1 assure analysis/test_dataset_definition_study_population.py

# Pharmacy First service (qualifier value)
pf_service_code = "983341000000102"
# Community Pharmacy (CP) Blood Pressure (BP) Check Service, not a PF code
bp_service_code = "1659111000000107"

registration = {
    "start_date": date(2020, 1, 1),
    "end_date": None,
    "practice_pseudo_id": 1,
}

test_data = {
    # PF consultation, in population
    1: {
        "practice_registrations": [registration],
        "clinical_events": [
            {"date": date(2024, 4, 1), "snomedct_code": pf_service_code},
        ],
        "expected_in_population": True,
        "expected_columns": {"practice_study_end": 1},
    },
    # No PF consultation, not in population
    2: {
        "practice_registrations": [registration],
        "clinical_events": [
            {"date": date(2024, 4, 1), "snomedct_code": bp_service_code},
        ],
        "expected_in_population": False,
    },
}
