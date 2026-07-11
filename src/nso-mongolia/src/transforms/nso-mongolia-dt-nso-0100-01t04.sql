-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Livestock type" AS livestock_type,
    "Aimags and the Capital" AS aimags_and_the_capital,
    CAST("Year" AS BIGINT) AS year,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-0100-01t04"
