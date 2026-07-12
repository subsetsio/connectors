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
    "Component" AS component,
    "Notes" AS notes
FROM "statswales-730344e1-9f46-421a-925e-89827910fa50"
