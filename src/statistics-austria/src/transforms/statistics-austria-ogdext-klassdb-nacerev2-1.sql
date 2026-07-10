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
    "ebene_erl",
    "titel_erl_uterungstext",
    "kurztitel",
    "titel",
    "korrespondenz_beschreibung",
    CAST("korrespondierende_ebene" AS BIGINT) AS korrespondierende_ebene,
    "korrespondierender_edv_code",
    "korrespondierender_code",
    "korrespondierender_titel"
FROM "statistics-austria-ogdext-klassdb-nacerev2-1"
