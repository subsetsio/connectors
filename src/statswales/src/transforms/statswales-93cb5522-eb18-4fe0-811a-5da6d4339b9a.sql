-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Welsh Skill" AS welsh_skill,
    "Local Authority" AS local_authority,
    strptime("Year", '%d/%m/%Y')::DATE AS year,
    "Notes" AS notes
FROM "statswales-93cb5522-eb18-4fe0-811a-5da6d4339b9a"
