-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "age_grp",
    "gender",
    "no_of_mbrs"
FROM "sg-data-d-782612851622c1643f94e3789d333e99"
