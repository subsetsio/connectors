-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Area code" AS area_code,
    "Area name" AS area_name,
    "Domain" AS domain,
    "Notes" AS notes
FROM "statswales-9706edd9-73ad-4902-bb12-7ccd7038626e"
