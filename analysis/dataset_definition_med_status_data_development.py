from ehrql import create_dataset, months, days
from ehrql.tables.tpp import patients, clinical_events
from ehrql.tables.raw.tpp import medications

from datetime import date

from codelists import *

dataset = create_dataset()
dataset.configure_dummy_data(population_size=1000)

dataset.define_population(patients.exists_for_patient())

# Pharmacy first clinical codes
pharmacy_first_event_codes = [
    "1659111000000107",
    "1659121000000101",
    "1577041000000109",
    "983341000000102",
]

# Combine all medication codelists
pharmacy_first_med_codes = (
    acute_otitis_media_tx_cod
    + impetigo_treatment_tx_cod
    + infected_insect_bites_tx_cod
    + shingles_treatment_tx_cod
    + sinusitis_tx_cod
    + sore_throat_tx_cod
    + urinary_tract_infection_tx_cod
)

# https://www.england.nhs.uk/primary-care/pharmacy/pharmacy-first/
pharmacy_first_launch_date = date(2024, 2, 1)

# Time interval for selecting medications pre and post Pharmacy First launch date
time_interval = months(6)

pharmacy_first_ids = clinical_events.where(
    clinical_events.snomedct_code.is_in(pharmacy_first_event_codes)
).consultation_id


# Select medications
# Pre launch, any medication
selected_medications_any_pre = medications.where(
    medications.date.is_on_or_between(
        pharmacy_first_launch_date - time_interval,
        pharmacy_first_launch_date - days(1),
    )
).sort_by(medications.date)

# Pre launch, pharmacy first medication (pfmed)
selected_medications_pfmed_pre = (
    medications.where(
        medications.date.is_on_or_between(
            pharmacy_first_launch_date - time_interval,
            pharmacy_first_launch_date - days(1),
        )
    )
    .where(medications.dmd_code.is_in(pharmacy_first_med_codes))
    .sort_by(medications.date)
)

# Pre launch, pharmacy first id (pdid) identified through clinical events
# and pharmacy first medication (pfmed)
selected_medications_pfmed_pfid_pre = (
    medications.where(
        medications.date.is_on_or_between(
            pharmacy_first_launch_date - time_interval,
            pharmacy_first_launch_date - days(1),
        )
    )
    .where(medications.dmd_code.is_in(pharmacy_first_med_codes))
    .where(medications.consultation_id.is_in(pharmacy_first_ids))
    .sort_by(medications.date)
)

# Post launch, any medication
selected_medications_any_post = medications.where(
    medications.date.is_on_or_between(
        pharmacy_first_launch_date, pharmacy_first_launch_date + time_interval
    )
).sort_by(medications.date)

# Post launch, pharmacy first medication (pfmed)
selected_medications_pfmed_post = (
    medications.where(
        medications.date.is_on_or_between(
            pharmacy_first_launch_date, pharmacy_first_launch_date + time_interval
        )
    )
    .where(medications.dmd_code.is_in(pharmacy_first_med_codes))
    .sort_by(medications.date)
)

# Post launch, pharmacy first id (pdid) identified through clinical events
# and pharmacy first medication (pfmed)
selected_medications_pfmed_pfid_post = (
    medications.where(
        medications.date.is_on_or_between(
            pharmacy_first_launch_date, pharmacy_first_launch_date + time_interval
        )
    )
    .where(medications.dmd_code.is_in(pharmacy_first_med_codes))
    .where(medications.consultation_id.is_in(pharmacy_first_ids))
    .sort_by(medications.date)
)

selected_medications_dict = {
    "pre_any": selected_medications_any_pre,
    "pre_pfmed": selected_medications_pfmed_pre,
    "pre_pfmedid": selected_medications_pfmed_pfid_pre,
    "post_any": selected_medications_any_post,
    "post_pfmed": selected_medications_pfmed_post,
    "post_pfmedid": selected_medications_pfmed_pfid_post,
}

# Count all medication status
# This will add 6 x 28 = 168 new columns
for desc, selected_medications in selected_medications_dict.items():
    for status in range(29):
        count_med_status_query = selected_medications.where(
            selected_medications.medication_status.is_in([status])
        ).count_for_patient()
        dataset.add_column(f"{desc}_status{status}", count_med_status_query)
