-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "day",
    "holiday"
FROM "sg-data-d-149b61ad0a22f61c09dc80f2df5bbec8"
