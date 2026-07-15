-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "NoWorkingPerson" AS noworkingperson,
    "Below_250" AS below_250,
    "250_499",
    "500_749",
    "750_999",
    "1_000_1_499",
    "1_500_1_999",
    "2_000_2_499",
    "2_500_2_999",
    "3_000andOver" AS 3_000andover
FROM "sg-data-d-43e23f6c3dd58c348869bfd732b2e939"
