-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Local authority" AS local_authority,
    "Tenure" AS tenure,
    "Notes" AS notes
FROM "statswales-3c14eab2-e102-4982-85bf-30262d5ab227"
