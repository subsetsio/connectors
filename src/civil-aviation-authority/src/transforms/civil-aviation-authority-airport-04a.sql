-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "rundate",
    "reporting_period",
    "reporting_airport_group_name",
    "reporting_airport_name",
    "total_atms",
    "total_cancelled_atms",
    "total_atms_excl_cancelled",
    "release_period",
    "family"
FROM "civil-aviation-authority-airport-04a"
