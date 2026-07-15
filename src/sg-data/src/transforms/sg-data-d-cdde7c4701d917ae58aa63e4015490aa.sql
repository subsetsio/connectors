-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "industry",
    "occupation",
    "retrench"
FROM "sg-data-d-cdde7c4701d917ae58aa63e4015490aa"
