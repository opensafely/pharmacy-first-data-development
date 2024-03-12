from ehrql import create_dataset, months, days
from ehrql.tables.tpp import patients
from ehrql.tables.raw.tpp import medications

from datetime import date

dataset = create_dataset()
dataset.define_population(patients.exists_for_patient())

# https://www.england.nhs.uk/primary-care/pharmacy/pharmacy-first/
pharmacy_first_launch_date = date(2024, 1, 31)

# Time interval for selecting medications pre and post Pharmacy First launch date
time_interval = months(3)

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

for time_interval_desc, selected_medications in selected_medications_dict.items():
    first_dmd_code_query = selected_medications.first_for_patient().dmd_code
    dataset.add_column(f"{time_interval_desc}_first_dmd_code", first_dmd_code_query)

for time_interval_desc, selected_medications in selected_medications_dict.items():
    first_med_status_query = selected_medications.first_for_patient().medication_status
    dataset.add_column(
        f"{time_interval_desc}_first_medication_status", first_med_status_query
    )
