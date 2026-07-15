-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "level_of_education",
    "level",
    "no_of_classes",
    "ave_class_size"
FROM "sg-data-d-bb5f828263a942a9af869eccf9b0068d"
