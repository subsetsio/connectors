-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Resident Health Board" AS resident_health_board,
    "Date" AS date,
    "Service" AS service,
    "Cumulative or quarterly count" AS cumulative_or_quarterly_count,
    "Notes" AS notes
FROM "statswales-c0af3a34-66d0-4d52-9f48-a683e096a399"
