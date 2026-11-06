from ehrql import codelist_from_csv

acute_otitis_media_tx_cod = codelist_from_csv(
    "codelists/opensafely-pharmacy-first-acute-otitis-media-treatment-full-dmd-codelist.csv",
    column="code",
)

impetigo_treatment_tx_cod = codelist_from_csv(
    "codelists/opensafely-pharmacy-first-impetigo-treatment-full-dmd-codelist.csv",
    column="code",
)

infected_insect_bites_tx_cod = codelist_from_csv(
    "codelists/opensafely-pharmacy-first-infected-insect-bites-treatment-full-dmd-codelist.csv",
    column="code",
)

shingles_treatment_tx_cod = codelist_from_csv(
    "codelists/opensafely-pharmacy-first-shingles-treatment-full-dmd-codelist.csv",
    column="code",
)

sinusitis_tx_cod = codelist_from_csv(
    "codelists/opensafely-pharmacy-first-sinusitis-treatment-full-dmd-codelist.csv",
    column="code",
)

sore_throat_tx_cod = codelist_from_csv(
    "codelists/opensafely-pharmacy-first-sore-throat-treatment-full-dmd-codelist.csv",
    column="code",
)

urinary_tract_infection_tx_cod = codelist_from_csv(
    "codelists/opensafely-pharmacy-first-urinary-tract-infection-treatment-full-dmd-codelist.csv",
    column="code",
)

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

pharmacy_first_event_codes = [
    # Community Pharmacist (CP) Consultation Service for minor illness (procedure)
    "1577041000000109",
    # Pharmacy First service (qualifier value)
    "983341000000102",
]