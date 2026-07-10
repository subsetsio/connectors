-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Vaccine" AS vaccine,
    "Geography Type" AS geography_type,
    "Geography" AS geography,
    "Survey Year/Influenza Season" AS survey_year_influenza_season,
    "Dimension Type" AS dimension_type,
    "Dimension" AS dimension,
    "Estimate (%)" AS estimate,
    CAST("Population Size" AS BIGINT) AS population_size
FROM "cdc-8w4j-reb4"
