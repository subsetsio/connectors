-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "grade",
    "family_guide_name",
    "link",
    "_language" AS language
FROM "nyc-open-data-fuvx-wqd7"
