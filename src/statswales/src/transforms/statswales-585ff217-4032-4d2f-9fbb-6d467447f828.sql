-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Collection Year (at 31 March)" AS collection_year_at_31_march,
    "Local Authority" AS local_authority,
    "Area Code" AS area_code,
    "Child Status" AS child_status,
    "Gender" AS gender,
    "Measure" AS measure,
    "Notes" AS notes
FROM "statswales-585ff217-4032-4d2f-9fbb-6d467447f828"
