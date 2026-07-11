-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "number_of_tankers",
    "gross_tonnage"
FROM "mpa-singapore-d-9adb5ace517591edd9a8c88291ac1f1c"
