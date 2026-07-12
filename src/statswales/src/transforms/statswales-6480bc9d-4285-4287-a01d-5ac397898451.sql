-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Quarter" AS quarter,
    "Local Health Board" AS local_health_board,
    "Contact" AS contact,
    "Notes" AS notes
FROM "statswales-6480bc9d-4285-4287-a01d-5ac397898451"
