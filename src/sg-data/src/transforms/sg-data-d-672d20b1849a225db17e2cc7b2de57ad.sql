-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "Below_2_000" AS below_2_000,
    "2_000_3_999",
    "4_000_5_999",
    "6_000_7_999",
    "8_000_9_999",
    "10_000_11_999",
    "12_000andOver" AS 12_000andover
FROM "sg-data-d-672d20b1849a225db17e2cc7b2de57ad"
