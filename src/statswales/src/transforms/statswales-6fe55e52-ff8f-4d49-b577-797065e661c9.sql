-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "local health board" AS local_health_board,
    "tumour site" AS tumour_site,
    "Notes" AS notes
FROM "statswales-6fe55e52-ff8f-4d49-b577-797065e661c9"
