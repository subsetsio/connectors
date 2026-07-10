-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Data Collection Period" AS data_collection_period,
    "Disability Type" AS disability_type,
    "Disability Status" AS disability_status,
    "Demographic Category" AS demographic_category,
    "Demographic" AS demographic,
    "Vaccination Status and Intent" AS vaccination_status_and_intent,
    CAST("Estimate (%)" AS DOUBLE) AS estimate,
    "95% CI (%)" AS 95_ci,
    CAST("Sample Size" AS BIGINT) AS sample_size,
    CAST("Suppression Flag" AS BIGINT) AS suppression_flag
FROM "cdc-muep-c3qd"
