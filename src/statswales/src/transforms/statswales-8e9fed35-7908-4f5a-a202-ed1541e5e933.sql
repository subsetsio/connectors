-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Deprivation group" AS deprivation_group,
    "National identity" AS national_identity,
    "Notes" AS notes
FROM "statswales-8e9fed35-7908-4f5a-a202-ed1541e5e933"
