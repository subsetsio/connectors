-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "local health board provider" AS local_health_board_provider,
    "specialty",
    "stage of pathway" AS stage_of_pathway,
    "age group" AS age_group,
    "Notes" AS notes
FROM "statswales-3ef3a1d8-1467-4afe-ad60-4fc3d92228a1"
