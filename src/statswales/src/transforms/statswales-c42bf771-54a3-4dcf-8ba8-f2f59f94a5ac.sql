-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Referral Source-Destination" AS referral_source_destination,
    "Location" AS location,
    "Notes" AS notes
FROM "statswales-c42bf771-54a3-4dcf-8ba8-f2f59f94a5ac"
