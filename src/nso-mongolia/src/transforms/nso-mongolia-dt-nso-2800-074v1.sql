-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "By urban and rural with soum center" AS by_urban_and_rural_with_soum_center,
    CAST("Time (Annual)" AS BIGINT) AS time_annual,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-2800-074v1"
