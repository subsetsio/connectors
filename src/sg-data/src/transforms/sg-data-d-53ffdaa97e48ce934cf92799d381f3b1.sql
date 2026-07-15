-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "maximum_rainfall_in_a_day"
FROM "sg-data-d-53ffdaa97e48ce934cf92799d381f3b1"
