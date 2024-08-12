from ehrql import INTERVAL, create_measures, months
from ehrql.tables.tpp import patients, clinical_events

measures = create_measures()

# Dictionary of pharmacy first codes
pharmacy_first_codes = {
    # Community Pharmacy (CP) Blood Pressure (BP) Check Service (procedure)
    "blood_pressure_service": ["1659111000000107"],
    # Community Pharmacy (CP) Contraception Service (procedure)
    "contraception_service": ["1659121000000101"],
    # Community Pharmacist (CP) Consultation Service for minor illness (procedure)
    "consultation_service": ["1577041000000109"],
    # Pharmacy First service (qualifier value)
    "pharmacy_first_service": ["983341000000102"],
}

selected_events = clinical_events.where(
    clinical_events.date.is_on_or_between(INTERVAL.start_date, INTERVAL.end_date)
)

# Count pharmacy first codes
pharmacy_first_code_counts = {}

for code_desc, code in pharmacy_first_codes.items():
    count_codes_query = selected_events.where(
        selected_events.snomedct_code.is_in(code)
    ).count_for_patient()
    pharmacy_first_code_counts[f"count_{code_desc}"] = count_codes_query

# Define intervals and measures
intervals = months(18).starting_on("2023-01-31")

for measures_name, code_counts in pharmacy_first_code_counts.items():
    measures.define_measure(
        name=measures_name,
        numerator=code_counts,
        denominator=patients.exists_for_patient(),
        intervals=intervals,
    )
