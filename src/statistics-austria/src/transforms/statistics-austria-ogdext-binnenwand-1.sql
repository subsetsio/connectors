-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "a10_2002",
    "grgemakt_10101",
    "grgemakt_10101_2",
    "staat_dichotom_1",
    "c11_1",
    CAST("c_277" AS BIGINT) AS c_277
FROM "statistics-austria-ogdext-binnenwand-1"
