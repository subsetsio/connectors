-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "start_year",
    "end_year",
    "flat_type",
    "no_of_completed_units"
FROM "sg-data-d-f97971e730d675ae046cc75690468c02"
