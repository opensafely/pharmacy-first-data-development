from ehrql import create_dataset, months, days
from ehrql.tables.tpp import patients, clinical_events
from ehrql.tables.raw.tpp import medications

from datetime import date

dataset = create_dataset()
dataset.define_population(patients.exists_for_patient())

# Dictionary of pharmacy first codes
pharmacy_first_dict = {
    # Community Pharmacy (CP) Blood Pressure (BP) Check Service (procedure)
    "comm_pharm_bp_service": ["1659111000000107"],
    # Community Pharmacy (CP) Contraception Service (procedure)
    "comm_pharm_contraception_service": ["1659121000000101"],
    # Community Pharmacist (CP) Consultation Service for minor illness (procedure)
    "comm_pharm_consultation_service": ["1577041000000109"],
    # Pharmacy First service (qualifier value)
    "pharm_first_service": ["983341000000102"],
}

med_status_dict = {
    "0": "Normal",
    "4": "Historical",
    "5": "Blue script",
    "6": "Private",
    "7": "Not in possession",
    "8": "Repeat dispensed",
    "9": "In possession",
    "10": "Dental",
    "11": "Hospital",
    "12": "Problem substance",
    "13": "From patient group direction",
    "14": "To take out",
    "15": "On admission",
    "16": "Regular medication",
    "17": "As required medication",
    "18": "Variable dose medication",
    "19": "Rate-controlled single regular",
    "20": "Only once",
    "21": "Outpatient",
    "22": "Rate-controlled multiple regular",
    "23": "Rate-controlled multiple only once",
    "24": "Rate-controlled single only once",
    "25": "Placeholder",
    "26": "Unconfirmed",
    "27": "Infusion",
    "28": "Reducing dose blue script"
    #"": "N/A"
}

pharmacy_first_codes = [
    code for codelist in pharmacy_first_dict.values() for code in codelist
]

# https://www.england.nhs.uk/primary-care/pharmacy/pharmacy-first/
pharmacy_first_launch_date = date(2024, 1, 31)

# Time interval for selecting medications pre and post Pharmacy First launch date
time_interval = months(3)

pharmacy_first_ids = clinical_events.where(
    clinical_events.snomedct_code.is_in(pharmacy_first_codes)
).consultation_id

# Select clinical events
selected_events_pre = (
    clinical_events.where(
        clinical_events.date.is_on_or_between(
            pharmacy_first_launch_date - time_interval,
            pharmacy_first_launch_date - days(1),
        )
    )
    .where(clinical_events.consultation_id.is_in(pharmacy_first_ids))
    .sort_by(clinical_events.date)
)

selected_events_post = (
    clinical_events.where(
        clinical_events.date.is_on_or_between(
            pharmacy_first_launch_date, pharmacy_first_launch_date + time_interval
        )
    )
    .where(clinical_events.consultation_id.is_in(pharmacy_first_ids))
    .sort_by(clinical_events.date)
)

selected_events_dict = {
    "pre": selected_events_pre,
    "post": selected_events_post,
}

# Select medications
selected_medications_pre = (
    medications.where(
        medications.date.is_on_or_between(
            pharmacy_first_launch_date - time_interval,
            pharmacy_first_launch_date - days(1),
        )
    )
    .where(medications.consultation_id.is_in(pharmacy_first_ids))
    .sort_by(medications.date)
)

selected_medications_post = (
    medications.where(
        medications.date.is_on_or_between(
            pharmacy_first_launch_date, pharmacy_first_launch_date + time_interval
        )
    )
    .where(medications.consultation_id.is_in(pharmacy_first_ids))
    .sort_by(medications.date)
)

selected_medications_dict = {
    "pre": selected_medications_pre,
    "post": selected_medications_post,
}

# Count distinct pharmacy first consultations per patient
for time_interval_desc, selected_events in selected_events_dict.items():
    count_distinct_consultations_query = (
        selected_events.consultation_id.count_distinct_for_patient()
    )
    dataset.add_column(
        f"{time_interval_desc}_count_distinct_consultations",
        count_distinct_consultations_query,
    )

# Get first medication status and dmd_code linked to pharmacy first consultation
for time_interval_desc, selected_medications in selected_medications_dict.items():
    first_dmd_code_query = selected_medications.first_for_patient().dmd_code
    first_med_status_query = selected_medications.first_for_patient().medication_status
    dataset.add_column(f"{time_interval_desc}_first_dmd_code", first_dmd_code_query)
    dataset.add_column(
        f"{time_interval_desc}_first_medication_status", first_med_status_query
    )

# Count pharmacy first codes
for code_desc, code in pharmacy_first_dict.items():
    for time_interval_desc, selected_events in selected_events_dict.items():
        count_codes_query = selected_events.where(
            selected_events.snomedct_code.is_in(code)
        ).count_for_patient()
        dataset.add_column(f"{time_interval_desc}_count_{code_desc}", count_codes_query)

# Get all medications over 1 year
selected_medications_any = (
    medications.where(
        medications.date.is_on_or_between(
            "2023-05-31",
            "2024-04-30",
        )
    )
)

# Count all medication statuses
for key, desc in med_status_dict.items():
    count_med_status_query = selected_medications_any.where(
        selected_medications_any.medication_status.is_in([int(key)])
    ).count_for_patient()
    dataset.add_column(
        f"count_medication_status_{desc}_{key}", count_med_status_query
    )