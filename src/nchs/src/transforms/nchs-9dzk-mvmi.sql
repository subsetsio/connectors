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
    "accidents_unintentional_injuries",
    "motor_vehicle_accidents",
    "intentional_self_harm_suicide",
    "assault_homicide",
    "drug_overdose",
    "covid_19_multiple_cause_of_death",
    "covid_19_underlying_cause_of_death",
    "flag_accid",
    "flag_mva",
    "flag_suic",
    "flag_homic",
    "flag_drugod"
FROM "nchs-9dzk-mvmi"
