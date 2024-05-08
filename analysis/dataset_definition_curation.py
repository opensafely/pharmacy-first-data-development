from ehrql import create_dataset, months, days
from ehrql.tables.tpp import patients, clinical_events
from ehrql.tables.raw.tpp import medications

from datetime import date

dataset = create_dataset()
dataset.define_population(patients.exists_for_patient())

# Dictionary of pharmacy first codes
pharmacy_first_codes = {
    # Community Pharmacy (CP) Blood Pressure (BP) Check Service (procedure)
    "comm_pharm_bp_service": ["1659111000000107"],
    # Community Pharmacy (CP) Contraception Service (procedure)
    "comm_pharm_contraception_service": ["1659121000000101"],
    # Community Pharmacist (CP) Consultation Service for minor illness (procedure)
    "comm_pharm_consultation_service": ["1577041000000109"],
    # Pharmacy First service (qualifier value)
    "pharm_first_service": ["983341000000102"],
}

# https://www.england.nhs.uk/primary-care/pharmacy/pharmacy-first/
pharmacy_first_launch_date = date(2024, 1, 31)

# Time interval for selecting medications pre and post Pharmacy First launch date
time_interval = months(3)

# Select medications
selected_medications_pre = medications.where(
    medications.date.is_on_or_between(
        pharmacy_first_launch_date - time_interval, pharmacy_first_launch_date - days(1)
    )
).sort_by(medications.date)

selected_medications_post = medications.where(
    medications.date.is_on_or_between(
        pharmacy_first_launch_date, pharmacy_first_launch_date + time_interval
    )
).sort_by(medications.date)

selected_medications_dict = {
    "pre": selected_medications_pre,
    "post": selected_medications_post,
}

# Select clinical events
selected_events_pre = clinical_events.where(
    clinical_events.date.is_on_or_between(
        pharmacy_first_launch_date - time_interval, pharmacy_first_launch_date - days(1)
    )
).sort_by(clinical_events.date)

selected_events_post = clinical_events.where(
    clinical_events.date.is_on_or_between(
        pharmacy_first_launch_date, pharmacy_first_launch_date + time_interval
    )
).sort_by(clinical_events.date)

selected_events_dict = {
    "pre": selected_events_pre,
    "post": selected_events_post,
}

# Add dataset variables from medications table
for time_interval_desc, selected_medications in selected_medications_dict.items():
    first_dmd_code_query = selected_medications.first_for_patient().dmd_code
    dataset.add_column(f"{time_interval_desc}_first_dmd_code", first_dmd_code_query)

for time_interval_desc, selected_medications in selected_medications_dict.items():
    first_med_status_query = selected_medications.first_for_patient().medication_status
    dataset.add_column(
        f"{time_interval_desc}_first_medication_status", first_med_status_query
    )

# Add dataset variables from clinical_events table
for code_desc, code in pharmacy_first_codes.items():
    for time_interval_desc, selected_events in selected_events_dict.items():
        count_codes_query = selected_events.where(
            selected_events.snomedct_code.is_in(code)
        ).count_for_patient()
        dataset.add_column(f"{time_interval_desc}_count_{code_desc}", count_codes_query)
