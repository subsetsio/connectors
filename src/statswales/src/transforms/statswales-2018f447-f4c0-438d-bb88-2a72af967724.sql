-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "School" AS school,
    "Local Authority" AS local_authority,
    "Sector" AS sector,
    "Type" AS type,
    "Governance" AS governance,
    "School Language" AS school_language,
    "Notes" AS notes
FROM "statswales-2018f447-f4c0-438d-bb88-2a72af967724"
