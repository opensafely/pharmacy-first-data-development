from ehrql import create_dataset
from ehrql.tables.tpp import clinical_events, practice_registrations

from codelists import pharmacy_first_event_codes

study_start = "2023-02-01"
study_end = "2026-02-28"

# Add more time points here to count registrations on other dates
index_dates = {
    "study_end": study_end,
}

dataset = create_dataset()
dataset.configure_dummy_data(population_size=1000)


# Practice is NULL when the patient is not registered on that date.
for time_point, date in index_dates.items():
    practice_id = practice_registrations.for_patient_on(date).practice_pseudo_id
    dataset.add_column(f"practice_{time_point}", practice_id)

dataset.define_population(has_pharmacy_first_consultation)
