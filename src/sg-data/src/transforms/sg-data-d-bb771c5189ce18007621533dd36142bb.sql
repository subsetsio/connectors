-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
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
    "8_000_8_999",
    "9_000_9_999",
    "10_000_10_999",
    "11_000_11_999",
    "12_000andOver" AS 12_000andover
FROM "sg-data-d-bb771c5189ce18007621533dd36142bb"
