-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Sector" AS sector,
    "Multiplier or effect type" AS multiplier_or_effect_type,
    "Notes" AS notes
FROM "statswales-3e1adeb5-de50-4dd6-abc8-5b9e7164739b"
