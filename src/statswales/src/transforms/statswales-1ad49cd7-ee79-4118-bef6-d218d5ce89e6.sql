-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Location" AS location,
    "Provider" AS provider,
    "Funding" AS funding,
    "Notes" AS notes
FROM "statswales-1ad49cd7-ee79-4118-bef6-d218d5ce89e6"
