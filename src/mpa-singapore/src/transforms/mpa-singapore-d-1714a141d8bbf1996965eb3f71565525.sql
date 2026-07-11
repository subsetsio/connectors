-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "category",
    "number_of_tankers",
    "gross_tonnage"
FROM "mpa-singapore-d-1714a141d8bbf1996965eb3f71565525"
