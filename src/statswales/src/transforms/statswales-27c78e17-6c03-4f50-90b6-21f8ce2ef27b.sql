-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "date",
    "local health board provider" AS local_health_board_provider,
    "local health board of residence" AS local_health_board_of_residence,
    "specialty",
    "stage of pathway" AS stage_of_pathway,
    "Notes" AS notes
FROM "statswales-27c78e17-6c03-4f50-90b6-21f8ce2ef27b"
