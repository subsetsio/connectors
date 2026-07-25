-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "nhtsa_action_number",
    "nhtsa_link",
    "manufacturer",
    "investigation_type",
    "subject",
    "component",
    "recall",
    CAST("open_date" AS TIMESTAMP) AS open_date,
    CAST("closed_date" AS TIMESTAMP) AS closed_date,
    "status"
FROM "u-s-department-of-transportation-b3rp-be92"
