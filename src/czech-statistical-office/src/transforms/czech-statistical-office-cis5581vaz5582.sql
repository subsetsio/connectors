-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This upstream relation table is currently empty; it is retained to preserve the accepted catalog surface if the source later publishes rows.
SELECT
    "kodjaz",
    "typvaz",
    "akrcis1",
    "kodcis1",
    "chodnota1",
    "text1",
    "akrcis2",
    "kodcis2",
    "chodnota2",
    "text2"
FROM "czech-statistical-office-cis5581vaz5582"
