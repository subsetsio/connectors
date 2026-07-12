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
    "weeks waiting" AS weeks_waiting,
    "age group" AS age_group,
    "Notes" AS notes
FROM "statswales-6bd7d5c9-844e-4e7c-85ba-7256e39f7214"
