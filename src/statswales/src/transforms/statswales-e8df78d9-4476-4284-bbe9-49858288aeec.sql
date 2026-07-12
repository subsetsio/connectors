-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Local Authority" AS local_authority,
    "Sector" AS sector,
    "Pay Range" AS pay_range,
    "Sex" AS sex,
    "Tenure" AS tenure,
    "Notes" AS notes
FROM "statswales-e8df78d9-4476-4284-bbe9-49858288aeec"
