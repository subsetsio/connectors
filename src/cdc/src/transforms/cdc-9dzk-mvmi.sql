-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Data As Of", '%m/%d/%Y')::DATE AS data_as_of,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date,
    "Jurisdiction of Occurrence" AS jurisdiction_of_occurrence,
    CAST("Year" AS BIGINT) AS year,
    CAST("Month" AS BIGINT) AS month,
    CAST("All Cause" AS BIGINT) AS all_cause,
    CAST("Natural Cause" AS BIGINT) AS natural_cause,
    CAST("Septicemia" AS BIGINT) AS septicemia,
    CAST("Malignant Neoplasms" AS BIGINT) AS malignant_neoplasms,
    CAST("Diabetes Mellitus" AS BIGINT) AS diabetes_mellitus,
    CAST("Alzheimer Disease" AS BIGINT) AS alzheimer_disease,
    CAST("Influenza and Pneumonia" AS BIGINT) AS influenza_and_pneumonia,
    CAST("Chronic Lower Respiratory Diseases" AS BIGINT) AS chronic_lower_respiratory_diseases,
    CAST("Other Diseases of Respiratory System" AS BIGINT) AS other_diseases_of_respiratory_system,
    CAST("Nephritis, Nephrotic Syndrome and Nephrosis" AS BIGINT) AS nephritis_nephrotic_syndrome_and_nephrosis,
    CAST("Symptoms, Signs and Abnormal Clinical and Laboratory Findings, Not Elsewhere Classified" AS BIGINT) AS symptoms_signs_and_abnormal_clinical_and_laboratory_findings_not_elsewhere_classified,
    CAST("Diseases of Heart" AS BIGINT) AS diseases_of_heart,
    CAST("Cerebrovascular Diseases" AS BIGINT) AS cerebrovascular_diseases,
    CAST("Accidents (Unintentional Injuries)" AS BIGINT) AS accidents_unintentional_injuries,
    CAST("Motor Vehicle Accidents" AS BIGINT) AS motor_vehicle_accidents,
    CAST("Intentional Self-Harm (Suicide)" AS BIGINT) AS intentional_self_harm_suicide,
    CAST("Assault (Homicide)" AS BIGINT) AS assault_homicide,
    CAST("Drug Overdose" AS BIGINT) AS drug_overdose,
    CAST("COVID-19 (Multiple Cause of Death)" AS BIGINT) AS covid_19_multiple_cause_of_death,
    CAST("COVID-19 (Underlying Cause of Death)" AS BIGINT) AS covid_19_underlying_cause_of_death,
    "flag_accid",
    "flag_mva",
    "flag_suic",
    "flag_homic",
    "flag_drugod"
FROM "cdc-9dzk-mvmi"
