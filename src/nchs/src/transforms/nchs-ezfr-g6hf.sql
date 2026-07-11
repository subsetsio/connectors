-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
SELECT
    "date_of_death_year",
    "date_of_death_month",
    "hhsregion",
    "agegroup",
    "allcause",
    "naturalcause",
    "septicemia_a40_a41",
    "malignant_neoplasms_c00_c97",
    "diabetes_mellitus_e10_e14",
    "alzheimer_disease_g30",
    "influenza_and_pneumonia_j09_j18",
    "chronic_lower_respiratory_diseases_j40_j47",
    "other_diseases_of_respiratory_system_j00_j06_j30_j39_j67_j70_j98",
    "nephritis_nephrotic_syndrome_and_nephrosis_n00_n07_n17_n19_n25_n27",
    "symptoms_signs_and_abnormal_clinical_and_laboratory_findings_not_elsewhere_classified_r00_r99",
    "diseases_of_heart_i00_i09_i11_i13_i20_i51",
    "cerebrovascular_diseases_i60_i69",
    "covid_19_u071_multiple_cause_of_death",
    "covid_19_u071_underlying_cause_of_death",
    strptime("analysisdate", '%m/%d/%Y')::DATE AS analysisdate,
    "note",
    "flag_allcause",
    "flag_natcause",
    "flag_sept",
    "flag_neopl",
    "flag_diab",
    "flag_alz",
    "flag_inflpn",
    "flag_clrd",
    "flag_otherresp",
    "flag_nephr",
    "flag_otherunk",
    "flag_hd",
    "flag_stroke",
    "flag_cov19mcod",
    "flag_cov19ucod"
FROM "nchs-ezfr-g6hf"
