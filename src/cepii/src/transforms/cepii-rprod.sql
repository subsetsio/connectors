-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Balassa-Samuelson measures are separate variants and should not be summed across measure sheets.
SELECT
    "measure",
    "Country" AS country,
    "Year" AS year,
    "indicator",
    "value"
FROM "cepii-rprod"
