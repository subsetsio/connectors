-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Geography" AS geography,
    "Sex" AS sex,
    "Notes" AS notes
FROM "statswales-eeeacb22-348b-4126-9421-504306a4cb55"
