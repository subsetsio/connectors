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
    "ma_einheit",
    "kurztitel",
    "korrespondierender_edv_code",
    CAST("korrespondierende_ebene" AS BIGINT) AS korrespondierende_ebene,
    "korrespondenz_beschreibung",
    "korrespondierender_titel",
    "korrespondierender_code"
FROM "statistics-austria-ogdext-klassdb-kn2017-1"
