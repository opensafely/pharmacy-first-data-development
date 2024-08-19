from ehrql import codelist_from_csv

acute_otitis_media_tx_cod = codelist_from_csv(
    "codelists/opensafely-pharmacy-first-acute-otitis-media-treatment-dmd.csv",
    column="code",
)

impetigo_treatment_tx_cod = codelist_from_csv(
    "codelists/opensafely-pharmacy-first-impetigo-treatment-dmd.csv",
    column="code",
)

infected_insect_bites_tx_cod = codelist_from_csv(
    "codelists/opensafely-pharmacy-first-infected-insect-bites-treatment-dmd.csv",
    column="code",
)

shingles_treatment_tx_cod = codelist_from_csv(
    "codelists/opensafely-pharmacy-first-shingles-treatment-dmd.csv",
    column="code",
)

sinusitis_tx_cod = codelist_from_csv(
    "codelists/opensafely-pharmacy-first-sinusitis-treatment-dmd.csv",
    column="code",
)

sore_throat_tx_cod = codelist_from_csv(
    "codelists/opensafely-pharmacy-first-sore-throat-treatment-dmd.csv",
    column="code",
)

urinary_tract_infection_tx_cod = codelist_from_csv(
    "codelists/opensafely-pharmacy-first-urinary-tract-infection-treatment-dmd.csv",
    column="code",
)

pf_clinical_pathway_conditions_cod = codelist_from_csv(
    "codelists/user-chriswood-pharmacy-first-clinical-pathway-conditions.csv",
    column="code",
)
