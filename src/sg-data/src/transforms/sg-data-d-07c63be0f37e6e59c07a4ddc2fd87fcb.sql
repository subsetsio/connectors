-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "salesperson_name",
    "registration_no",
    "registration_start_date",
    "registration_end_date",
    "estate_agent_name",
    "estate_agent_license_no"
FROM "sg-data-d-07c63be0f37e6e59c07a4ddc2fd87fcb"
