-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yr",
    "age_grp",
    "sex",
    "no_of_mbrs"
FROM "sg-data-d-09db49ac4034d4be26b4930b16749005"
