-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("data_as_of", '%m/%d/%Y')::DATE AS data_as_of,
    "start_date",
    strptime("end_date", '%m/%d/%Y')::DATE AS end_date,
    "jurisdiction_of_occurrence",
    "year",
    "month",
    "race_and_hispanic_origin_group",
    "age_group",
    "all_cause",
    "natural_cause",
    "septicemia",
    "malignant_neoplasms",
    "diabetes_mellitus",
    "alzheimer_disease",
    "influenza_and_pneumonia",
    "chronic_lower_respiratory_diseases",
    "other_diseases_of_respiratory_system",
    "nephritis_nephrotic_syndrome_and_nephrosis",
    "symptoms_signs_and_abnormal_clinical_and_laboratory_findings_not_elsewhere_classified",
    "diseases_of_heart",
    "cerebrovascular_diseases",
    "covid_19_multiple_cause_of_death",
    "covid_19_underlying_cause_of_death"
FROM "nchs-r5pw-bk5t"
