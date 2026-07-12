-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Collection Year (at 31 March)" AS collection_year_at_31_march,
    "Local Authority" AS local_authority,
    "Area Code" AS area_code,
    "Child Status" AS child_status,
    "Component" AS component,
    "Notes" AS notes
FROM "statswales-e4c32b9c-9bc7-4dd9-8a2b-8f95e24fc552"
