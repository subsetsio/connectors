-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "By aimags and the capital" AS by_aimags_and_the_capital,
    CAST("Time (Annual)" AS BIGINT) AS time_annual,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-2800-058v1"
