-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "contact_id",
    "city",
    "state",
    "postal_code",
    "council_member",
    "community_board",
    "case_id",
    "case_type",
    "subtypes",
    "case_subject",
    "case_start_date",
    "case_end_date",
    "case_status"
FROM "nyc-open-data-39qw-754y"
