from ehrql import create_dataset
from ehrql.tables.tpp import patients, clinical_events

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

selected_events = clinical_events.where(
    clinical_events.date.is_on_or_between("2020-04-01", "2024-03-31")
)

# Add one count variable for each code
for code_desc, code in pharmacy_first_codes.items():
    count_codes_query = selected_events.where(
        selected_events.snomedct_code.is_in(code)
    ).count_for_patient()
    dataset.add_column(f"count_{code_desc}", count_codes_query)
