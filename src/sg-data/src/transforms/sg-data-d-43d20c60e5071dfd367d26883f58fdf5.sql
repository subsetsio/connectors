-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sex",
    "highest_qualification_attained",
    "age",
    "employed"
FROM "sg-data-d-43d20c60e5071dfd367d26883f58fdf5"
