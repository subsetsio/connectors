-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "period_of_gestation",
    "birth_weight",
    "gender",
    "type_of_birth",
    "birth_count"
FROM "sg-data-d-88039c470472a9a79da2fc662c33c48c"
