-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Vaccine" AS vaccine,
    "Geography Type" AS geography_type,
    "Geography" AS geography,
    "Season" AS season,
    "Personnel Type" AS personnel_type,
    CAST("Estimate (%)" AS DOUBLE) AS estimate,
    "95% CI (%)" AS 95_ci,
    CAST("Sample Size" AS BIGINT) AS sample_size
FROM "cdc-xerk-pcm8"
