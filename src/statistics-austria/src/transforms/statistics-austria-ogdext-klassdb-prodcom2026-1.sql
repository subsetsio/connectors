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
    "ma_einheit2",
    "liste_prodcom",
    "kurztitel",
    CAST("korrespondierende_ebene" AS BIGINT) AS korrespondierende_ebene,
    "korrespondenz_beschreibung",
    "korrespondierender_code",
    "korrespondierender_edv_code",
    "korrespondierender_titel"
FROM "statistics-austria-ogdext-klassdb-prodcom2026-1"
