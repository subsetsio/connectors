-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "weight",
    "mother_age",
    "gender",
    "birth_count"
FROM "sg-data-d-deb91bee190b87e7d3345d341f47d6a5"
