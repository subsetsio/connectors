-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "NoWorkingPerson" AS noworkingperson,
    "Below_1_000" AS below_1_000,
    "1_000_1_999",
    "2_000_2_999",
    "3_000_3_999",
    "4_000_4_999",
    "5_000_5_999",
    "6_000_6_999",
    "7_000_7_999",
    "8_000_8_999",
    "9_000_9_999",
    "10_000_10_999",
    "11_000_11_999",
    "12_000_12_999",
    "13_000_13_999",
    "14_000_14_999",
    "15_000_17_499",
    "17_500_19_999",
    "20_000andOver" AS 20_000andover
FROM "sg-data-d-e2e2421777b5c2b6aff5db721d3dfabc"
