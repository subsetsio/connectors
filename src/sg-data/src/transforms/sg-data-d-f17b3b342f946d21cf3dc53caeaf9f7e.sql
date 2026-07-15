-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "ind1",
    "ind2",
    "avc"
FROM "sg-data-d-f17b3b342f946d21cf3dc53caeaf9f7e"
