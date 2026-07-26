-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "candidate_borodist",
    "classification",
    "_statement" AS statement,
    "due_date",
    "status",
    "days_late"
FROM "nyc-open-data-2ujk-6z7u"
