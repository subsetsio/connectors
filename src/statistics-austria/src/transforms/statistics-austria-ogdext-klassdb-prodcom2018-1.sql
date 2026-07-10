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
    "titel",
    "ma_einheit2",
    "korrespondierender_titel",
    "liste_prodcom",
    CAST("korrespondierende_ebene" AS BIGINT) AS korrespondierende_ebene,
    "korrespondenz_beschreibung",
    "ma_einheit",
    "korrespondierender_edv_code",
    "korrespondierender_code"
FROM "statistics-austria-ogdext-klassdb-prodcom2018-1"
