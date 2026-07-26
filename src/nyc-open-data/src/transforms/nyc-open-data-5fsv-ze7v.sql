-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "meeting_date",
    "project_id",
    "title",
    "borough",
    "lead_agency",
    "secondary_agency",
    "public_private",
    "project_type",
    "construction_type",
    "result",
    "review_cycles",
    "previous_year_submission"
FROM "nyc-open-data-5fsv-ze7v"
