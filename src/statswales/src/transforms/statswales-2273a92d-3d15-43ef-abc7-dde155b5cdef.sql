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
    "Housing type" AS housing_type,
    "Funding" AS funding,
    "Notes" AS notes
FROM "statswales-2273a92d-3d15-43ef-abc7-dde155b5cdef"
