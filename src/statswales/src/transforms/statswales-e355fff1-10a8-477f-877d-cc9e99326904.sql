-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Service Category" AS service_category,
    "Service Type" AS service_type,
    "Local Authority" AS local_authority,
    "Local Health Board" AS local_health_board,
    "Notes" AS notes
FROM "statswales-e355fff1-10a8-477f-877d-cc9e99326904"
