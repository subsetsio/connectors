-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Only parks with a published attendance table are represented; join to the parks table for the broader Queue Times park directory.
SELECT
    "park_id",
    "park_name",
    "year",
    "annual_attendance"
FROM "park-attendance-attendance"
