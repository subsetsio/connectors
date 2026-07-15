-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "Chinese" AS chinese,
    "Malays" AS malays,
    "Indians" AS indians,
    "Others" AS others
FROM "sg-data-d-e5de9776d19b810f5df454d31e0b74d5"
