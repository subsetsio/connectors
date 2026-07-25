-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "modal_administration",
    "urban_rural",
    "project_name",
    "applicant",
    CAST("round" AS TIMESTAMP) AS round,
    "capital_vs_planning",
    "project_type",
    "project_description",
    CAST("amount" AS DOUBLE) AS amount,
    "location_precision",
    "location_1",
    "location_1_address",
    "location_1_city",
    "location_1_state",
    "location_1_zip"
FROM "u-s-department-of-transportation-g43q-hx7i"
