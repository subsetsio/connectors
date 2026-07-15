-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sector",
    "sub_sector",
    "ng_consumption_tj"
FROM "sg-data-d-8ffdcb4ec69ae1951f4a0d2701a16f4d"
