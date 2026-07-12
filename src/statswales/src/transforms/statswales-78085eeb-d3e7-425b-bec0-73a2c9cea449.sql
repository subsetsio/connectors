-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Local Authority" AS local_authority,
    "Year" AS year,
    "Type of course" AS type_of_course,
    "Notes" AS notes
FROM "statswales-78085eeb-d3e7-425b-bec0-73a2c9cea449"
