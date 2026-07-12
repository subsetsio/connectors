-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Parity" AS parity,
    "Breastfeeding status" AS breastfeeding_status,
    "Notes" AS notes
FROM "statswales-53027b0e-7619-4e49-a060-68ca598cea26"
