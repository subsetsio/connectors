-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "Average_no_of_training_hours_per_inmate_trained_per_year" AS average_no_of_training_hours_per_inmate_trained_per_year,
    "no_of_inmates_trained"
FROM "sg-data-d-020be791f1cd0ca61e749c43e5dde1a2"
