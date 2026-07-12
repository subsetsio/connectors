-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Mode of onset of labour" AS mode_of_onset_of_labour,
    "Epidurals" AS epidurals,
    "Notes" AS notes
FROM "statswales-5eb9315c-d8fa-44c8-9479-b6f9bd184cc9"
