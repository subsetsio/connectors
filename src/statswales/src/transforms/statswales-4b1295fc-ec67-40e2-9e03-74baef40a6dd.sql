-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Location" AS location,
    "Public sector land" AS public_sector_land,
    "Funding" AS funding,
    "Notes" AS notes
FROM "statswales-4b1295fc-ec67-40e2-9e03-74baef40a6dd"
