-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "instrument_type",
    "no_of_instrument",
    "stamp_duty_assessed"
FROM "sg-data-d-fbca086bcaf80adb75e907e3d7b92f64"
