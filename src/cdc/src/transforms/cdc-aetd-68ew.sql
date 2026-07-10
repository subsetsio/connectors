-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Vaccine" AS vaccine,
    "Dose" AS dose,
    "Geography Type" AS geography_type,
    "Geography" AS geography,
    "FIPS" AS fips,
    CAST("Survey Year" AS BIGINT) AS survey_year,
    "Dimension Type" AS dimension_type,
    "Dimension" AS dimension,
    "Estimate (%)" AS estimate,
    "95% CI (%)" AS 95_ci,
    CAST("Sample Size" AS BIGINT) AS sample_size
FROM "cdc-aetd-68ew"
