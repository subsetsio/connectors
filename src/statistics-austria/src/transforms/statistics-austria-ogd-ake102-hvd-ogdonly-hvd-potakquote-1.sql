-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time_serie" AS BIGINT) AS time_serie,
    "quota_classifications",
    "labour_reserve_seeking_but_not_available",
    "labour_reserve_available_but_not_seeking"
FROM "statistics-austria-ogd-ake102-hvd-ogdonly-hvd-potakquote-1"
