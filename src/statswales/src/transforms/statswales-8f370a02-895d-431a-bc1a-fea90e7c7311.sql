-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Disabled or non-disabled people" AS disabled_or_non_disabled_people,
    "Sex" AS sex,
    "Notes" AS notes
FROM "statswales-8f370a02-895d-431a-bc1a-fea90e7c7311"
