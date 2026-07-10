-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("ebene" AS BIGINT) AS ebene,
    "edv_code",
    "code",
    "kurztitel",
    "ma_einheit",
    "titel",
    "ma_einheit2",
    "liste_prodcom"
FROM "statistics-austria-ogdext-klassdb-prodcom2017-1"
