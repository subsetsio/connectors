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
    "Notes" AS notes
FROM "statswales-3bcabf3f-fbf9-4fd0-816f-9ea6041817a3"
