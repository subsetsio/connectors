-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Local health board" AS local_health_board,
    "Tumour site" AS tumour_site,
    "Sex" AS sex,
    "Age group" AS age_group,
    "Notes" AS notes
FROM "statswales-394da9f2-b879-4994-94de-577d8f863247"
