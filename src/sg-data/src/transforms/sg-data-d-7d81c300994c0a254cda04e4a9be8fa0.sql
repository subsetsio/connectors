-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "regrossed_bal_grp",
    "no_of_active_mbrs"
FROM "sg-data-d-7d81c300994c0a254cda04e4a9be8fa0"
