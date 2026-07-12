-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Welsh Index of Multiple Deprivation quintile" AS welsh_index_of_multiple_deprivation_quintile,
    "Breastfeeding status" AS breastfeeding_status,
    "Notes" AS notes
FROM "statswales-15dd1b8d-0837-43ce-9977-f79cf83ec797"
