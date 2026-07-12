-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Local Authority" AS local_authority,
    CAST("Year" AS BIGINT) AS year,
    "Flying start status" AS flying_start_status,
    "Breastfeeding status" AS breastfeeding_status,
    "Notes" AS notes
FROM "statswales-7271f10f-a55a-4869-b3f1-c3b8b99edad3"
