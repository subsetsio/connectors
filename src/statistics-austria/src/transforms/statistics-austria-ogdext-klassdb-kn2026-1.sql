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
    "titel",
    CAST("korrespondierende_ebene" AS BIGINT) AS korrespondierende_ebene,
    "korrespondierender_edv_code",
    "korrespondierender_code",
    "korrespondierender_titel",
    "korrespondenz_beschreibung",
    "ma_einheit",
    "kurztitel"
FROM "statistics-austria-ogdext-klassdb-kn2026-1"
