-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "mother_race",
    "mother_education",
    "birth_order",
    "birth_count"
FROM "sg-data-d-36149d0682172bc5e7c93ad44b8ab418"
