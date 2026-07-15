-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "eweek",
    "type_dengue",
    "number"
FROM "sg-data-d-ac1eecf0886ff0bceefbc51556247015"
