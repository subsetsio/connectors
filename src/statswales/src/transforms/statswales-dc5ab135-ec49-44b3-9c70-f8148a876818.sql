-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    strptime("Date", '%d/%m/%Y')::DATE AS date,
    "Staff" AS staff,
    "Ability" AS ability,
    "Welsh skill" AS welsh_skill,
    "Local health board" AS local_health_board,
    "Notes" AS notes
FROM "statswales-dc5ab135-ec49-44b3-9c70-f8148a876818"
