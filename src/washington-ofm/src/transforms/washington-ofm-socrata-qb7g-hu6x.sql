-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_entity_id" AS entity_id,
    "_source_type" AS source_type,
    "_socrata_dataset_id" AS socrata_dataset_id,
    "county",
    "to_sort_by_county_and_year",
    CAST("to_sort_by_year_and_county" AS BIGINT) AS to_sort_by_year_and_county,
    CAST("year" AS BIGINT) AS year,
    "state_and_county_fips_code",
    CAST("alzheimer_s_disease_dementia_prevalence" AS DOUBLE) AS alzheimer_s_disease_dementia_prevalence,
    CAST("arthritis_prevalence" AS DOUBLE) AS arthritis_prevalence,
    CAST("asthma_prevalence" AS DOUBLE) AS asthma_prevalence,
    CAST("atrial_fibrillation_prevalence" AS DOUBLE) AS atrial_fibrillation_prevalence,
    CAST("autism_spectrum_disorders_prevalence" AS DOUBLE) AS autism_spectrum_disorders_prevalence,
    CAST("copd_prevalence" AS DOUBLE) AS copd_prevalence,
    CAST("cancer_prevalence" AS DOUBLE) AS cancer_prevalence,
    CAST("chronic_kidney_disease_prevalence" AS DOUBLE) AS chronic_kidney_disease_prevalence,
    CAST("depression_prevalence" AS DOUBLE) AS depression_prevalence,
    CAST("diabetes_prevalence" AS DOUBLE) AS diabetes_prevalence,
    CAST("hiv_aids_prevalence" AS DOUBLE) AS hiv_aids_prevalence,
    CAST("heart_failure_prevalence" AS DOUBLE) AS heart_failure_prevalence,
    CAST("hepatitis_chronic_viral_b_c_prevalence" AS DOUBLE) AS hepatitis_chronic_viral_b_c_prevalence,
    CAST("hyperlipidemia_prevalence" AS DOUBLE) AS hyperlipidemia_prevalence,
    CAST("hypertension_prevalence" AS DOUBLE) AS hypertension_prevalence,
    CAST("ischemic_heart_disease_prevalence" AS DOUBLE) AS ischemic_heart_disease_prevalence,
    CAST("osteoporosis_prevalence" AS DOUBLE) AS osteoporosis_prevalence,
    CAST("schizophrenia_other_psychotic_disorders_prevalence" AS DOUBLE) AS schizophrenia_other_psychotic_disorders_prevalence,
    CAST("stroke_prevalence" AS DOUBLE) AS stroke_prevalence
FROM "washington-ofm-socrata-qb7g-hu6x"
