-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sector",
    "specialist_non-specialist" AS specialist_non_specialist,
    "count"
FROM "sg-data-d-4a15de043d48bf829b6d97c6068bbf03"
