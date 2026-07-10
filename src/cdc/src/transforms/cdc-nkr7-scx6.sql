-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Month" AS month,
    "Flu Season" AS flu_season,
    "Race_Ethnicity" AS race_ethnicity,
    CAST("Percentage Vaccinated" AS DOUBLE) AS percentage_vaccinated
FROM "cdc-nkr7-scx6"
