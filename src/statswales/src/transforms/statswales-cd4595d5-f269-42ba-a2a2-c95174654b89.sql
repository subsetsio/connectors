-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    strptime("Census date", '%d/%m/%Y')::DATE AS census_date,
    "Local health board" AS local_health_board,
    "Age group" AS age_group,
    "Sex" AS sex,
    "Notes" AS notes
FROM "statswales-cd4595d5-f269-42ba-a2a2-c95174654b89"
