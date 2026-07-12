-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Local health board of residence" AS local_health_board_of_residence,
    "Local health board provider" AS local_health_board_provider,
    "Specialty" AS specialty,
    "Grouped weeks waiting" AS grouped_weeks_waiting,
    "Notes" AS notes
FROM "statswales-5b27909c-ed0f-408e-98d9-bd0485ec8990"
