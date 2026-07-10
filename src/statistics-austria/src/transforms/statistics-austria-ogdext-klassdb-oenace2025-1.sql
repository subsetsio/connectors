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
    "alphabetikumsbegriff",
    "t_tigkeit",
    "akt_gut",
    "korrespondierender_code",
    "korrespondierender_titel",
    "titel",
    "ebene_erl",
    "korrespondierender_edv_code",
    "korrespondenz_beschreibung",
    "titel_erl_uterungstext",
    "korrespondierende_ebene",
    "kurztitel"
FROM "statistics-austria-ogdext-klassdb-oenace2025-1"
