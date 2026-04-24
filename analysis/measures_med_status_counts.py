from ehrql import create_dataset, months, days, INTERVAL, create_measures
from ehrql.tables.tpp import patients, clinical_events
from ehrql.tables.raw.tpp import medications

from codelists import pharmacy_first_event_codes
measures = create_measures()
start_date = "2023-08-01"
monthly_intervals = 32

pharmacy_first_ids = clinical_events.where(clinical_events.snomedct_code.is_in(pharmacy_first_event_codes)).consultation_id

pf_medications = medications.where(medications.consultation_id.is_in(pharmacy_first_ids)).where(medications.date.is_on_or_between(INTERVAL.start_date, INTERVAL.end_date)).sort_by(medications.date).first_for_patient()
medication_status = pf_medications.medication_status

measures.define_measure(
    name="pf_medications_by_med_status",
    numerator=pf_medications.count_for_patient(),
    denominator=pf_medications.count_for_patient(),
    group_by={"medication_status": medication_status},
    intervals=months(monthly_intervals).starting_on(start_date),
)