-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_name",
    "operator_name",
    "contact_number",
    "bus_operator_email",
    "bus_fare_info"
FROM "sg-data-d-a9e4d1b0f2897b4480723bf7f074c5e5"
