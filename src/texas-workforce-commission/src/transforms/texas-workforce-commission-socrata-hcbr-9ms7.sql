-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "provider_name",
    "description_of_provider",
    "provider_url",
    "campus_name",
    "campus_address1",
    "campus_city",
    "campus_state",
    CAST("campus_zip_code" AS BIGINT) AS campus_zip_code,
    "campus_county",
    "program_name",
    "program_description",
    "length_contact_hours",
    "length_weeks",
    "program_format",
    CAST("required_cost_tuition_fees" AS BIGINT) AS required_cost_tuition_fees,
    "campus_address2"
FROM "texas-workforce-commission-socrata-hcbr-9ms7"
