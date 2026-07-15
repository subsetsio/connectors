-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "Below_1_000" AS below_1_000,
    "1_000_1_499",
    "1_500_1_999",
    "2_000_2_499",
    "2_500_2_999",
    "3_000_3_999",
    "4_000_4_999",
    "5_000_5_999",
    "6_000_6_999",
    "7_000_7_999",
    "8_000andOver" AS 8_000andover
FROM "sg-data-d-d59ed9cc61560544973393078baf74b0"
