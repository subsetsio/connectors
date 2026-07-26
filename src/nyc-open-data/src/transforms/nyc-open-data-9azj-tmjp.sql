-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "_name" AS name,
    "description",
    "frequency",
    "local_law",
    "charter_code",
    "last_published_date",
    "see_all_reports"
FROM "nyc-open-data-9azj-tmjp"
