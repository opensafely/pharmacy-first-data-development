from datetime import date
from analysis.dataset_definition_med_status_data_development import dataset

# Run the following command in the terminal to test the dataset definition dataset_definition_med_status_data_development
# opensafely exec ehrql:v1 assure analysis/test_dataset_definition_med_status_data_development.py

# Pharmacy First service (qualifier value)
pf_service_code = "983341000000102"
# Community Pharmacist (CP) Consultation Service for minor illness (procedure)
pf_consultation_code = "1577041000000109"
# Community Pharmacy (CP) Blood Pressure (BP) Check Service, not a PF code
bp_service_code = "1659111000000107"
# Phenoxymethylpenicillin 250mg/5ml oral solution, in the PF medication codelists
pf_med_code = "20129711000001103"
non_pf_med_code = "Non-PF Medication"


test_data = {
    # Pre-launch PF consultation with a PF medication in the same consultation
    1: {
        "patients": {"date_of_birth": date(1950, 1, 1)},
        "clinical_events": [
            {
                "consultation_id": 1,
                "date": date(2024, 1, 10),
                "snomedct_code": pf_service_code,
            },
        ],
        "medications_raw": [
            {
                "consultation_id": 1,
                "date": date(2024, 1, 10),
                "dmd_code": pf_med_code,
                "medication_status": 4,
            },
        ],
        "expected_in_population": True,
        "expected_columns": {
            "pre_anymed_status4": 1,
            "pre_anypfid_status4": 1,
            "pre_anypfdate_status4": 1,
            "pre_pfmed_status4": 1,
            "pre_pfmedid_status4": 1,
            "pre_pfmedpfdate_status4": 1,
            "post_anymed_status4": 0,
            "post_anypfid_status4": 0,
            "post_anypfdate_status4": 0,
            "post_pfmed_status4": 0,
            "post_pfmedid_status4": 0,
            "post_pfmedpfdate_status4": 0,
        },
    },
    # Post-launch PF consultation with three medications
    2: {
        "patients": {"date_of_birth": date(1950, 1, 1)},
        "clinical_events": [
            {
                "consultation_id": 1,
                "date": date(2024, 4, 1),
                "snomedct_code": pf_consultation_code,
            },
        ],
        "medications_raw": [
            {
                # PF medication, same consultation and same day
                "consultation_id": 1,
                "date": date(2024, 4, 1),
                "dmd_code": pf_med_code,
                "medication_status": 4,
            },
            {
                # Non-PF medication, different consultation but same day
                "consultation_id": 2,
                "date": date(2024, 4, 1),
                "dmd_code": non_pf_med_code,
                "medication_status": 0,
            },
            {
                # PF medication, different consultation and different day
                "consultation_id": 3,
                "date": date(2024, 4, 10),
                "dmd_code": pf_med_code,
                "medication_status": 0,
            },
        ],
        "expected_in_population": True,
        "expected_columns": {
            "post_anymed_status4": 1,
            "post_anypfid_status4": 1,
            "post_anypfdate_status4": 1,
            "post_pfmed_status4": 1,
            "post_pfmedid_status4": 1,
            "post_pfmedpfdate_status4": 1,
            "post_anymed_status0": 2,
            "post_anypfid_status0": 0,
            "post_anypfdate_status0": 1,
            "post_pfmed_status0": 1,
            "post_pfmedid_status0": 0,
            "post_pfmedpfdate_status0": 0,
            "pre_anymed_status4": 0,
            "pre_anypfid_status4": 0,
            "pre_anypfdate_status4": 0,
            "pre_pfmed_status4": 0,
            "pre_pfmedid_status4": 0,
            "pre_pfmedpfdate_status4": 0,
            "pre_anymed_status0": 0,
            "pre_anypfid_status0": 0,
            "pre_anypfdate_status0": 0,
            "pre_pfmed_status0": 0,
            "pre_pfmedid_status0": 0,
            "pre_pfmedpfdate_status0": 0,
        },
    },
    # Post-launch PF medication in a consultation without a PF code
    3: {
        "patients": {"date_of_birth": date(1950, 1, 1)},
        "clinical_events": [
            {
                "consultation_id": 1,
                "date": date(2024, 4, 1),
                "snomedct_code": bp_service_code,
            },
        ],
        "medications_raw": [
            {
                "consultation_id": 1,
                "date": date(2024, 4, 1),
                "dmd_code": pf_med_code,
                "medication_status": 3,
            },
        ],
        "expected_in_population": True,
        "expected_columns": {
            "post_anymed_status3": 1,
            "post_anypfid_status3": 0,
            "post_anypfdate_status3": 0,
            "post_pfmed_status3": 1,
            "post_pfmedid_status3": 0,
            "post_pfmedpfdate_status3": 0,
            "pre_anymed_status3": 0,
            "pre_anypfid_status3": 0,
            "pre_anypfdate_status3": 0,
            "pre_pfmed_status3": 0,
            "pre_pfmedid_status3": 0,
            "pre_pfmedpfdate_status3": 0,
        },
    },
    # Medications on and around the edges of the pre and post periods
    4: {
        "patients": {"date_of_birth": date(1950, 1, 1)},
        "clinical_events": [],
        "medications_raw": [
            {
                # Day before the pre period starts
                "consultation_id": 1,
                "date": date(2023, 7, 31),
                "dmd_code": non_pf_med_code,
                "medication_status": 0,
            },
            {
                # Last day of the pre period
                "consultation_id": 2,
                "date": date(2024, 1, 31),
                "dmd_code": non_pf_med_code,
                "medication_status": 0,
            },
            {
                # Launch day, first day of the post period
                "consultation_id": 3,
                "date": date(2024, 2, 1),
                "dmd_code": non_pf_med_code,
                "medication_status": 0,
            },
            {
                # Day after the post period ends
                "consultation_id": 4,
                "date": date(2026, 3, 2),
                "dmd_code": non_pf_med_code,
                "medication_status": 0,
            },
        ],
        "expected_in_population": True,
        "expected_columns": {
            "pre_anymed_status0": 1,
            "pre_anypfid_status0": 0,
            "pre_anypfdate_status0": 0,
            "pre_pfmed_status0": 0,
            "pre_pfmedid_status0": 0,
            "pre_pfmedpfdate_status0": 0,
            "post_anymed_status0": 1,
            "post_anypfid_status0": 0,
            "post_anypfdate_status0": 0,
            "post_pfmed_status0": 0,
            "post_pfmedid_status0": 0,
            "post_pfmedpfdate_status0": 0,
        },
    },
}
