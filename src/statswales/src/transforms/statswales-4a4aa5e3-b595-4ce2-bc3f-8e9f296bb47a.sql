-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Local Authority" AS local_authority,
    "School Type" AS school_type,
    "Notes" AS notes
FROM "statswales-4a4aa5e3-b595-4ce2-bc3f-8e9f296bb47a"
