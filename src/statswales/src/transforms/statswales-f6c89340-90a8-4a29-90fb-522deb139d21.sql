-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Data values" AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Geography" AS geography,
    "Notes" AS notes
FROM "statswales-f6c89340-90a8-4a29-90fb-522deb139d21"
