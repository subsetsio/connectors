-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    strptime("Date", '%d/%m/%Y')::DATE AS date,
    "Local health board" AS local_health_board,
    "Ability" AS ability,
    "Welsh skill" AS welsh_skill,
    "Notes" AS notes
FROM "statswales-f670ec3e-f46c-444e-816d-83da35ef2e43"
