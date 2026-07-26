-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "permit_number",
    "schedule_date",
    "schedule_time",
    "base_number",
    "last_updated_date",
    "last_updated_time"
FROM "nyc-open-data-rdxc-q253"
