-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "member_id",
    "first_name",
    "last_name",
    "full_name",
    "committee",
    "appointment_type",
    "start_date",
    "end_date",
    "modified_date",
    "committee_id",
    "id"
FROM "nyc-open-data-aabe-yfm9"
