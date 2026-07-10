-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Vaccine/Sample" AS vaccine_sample,
    "Dose" AS dose,
    "Geography Type" AS geography_type,
    "Geography" AS geography,
    "Survey Year" AS survey_year,
    "Dimension Type" AS dimension_type,
    "Dimension" AS dimension,
    "Estimate (%)" AS estimate,
    "95% CI (%)" AS 95_ci,
    CAST("Sample Size" AS BIGINT) AS sample_size
FROM "cdc-ee48-w5t6"
