-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "calendar_year",
    "type_of_stamp_duty",
    "no_of_transactions",
    "stamp_duty_assessed"
FROM "sg-data-d-38070327ca83c81887289a5c09d3c545"
