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
    "korrespondierender_titel",
    "ebene_erl",
    "titel",
    "korrespondierende_ebene",
    "titel_erl_uterungstext",
    "kurztitel",
    "korrespondierender_code",
    "korrespondierender_edv_code",
    "korrespondenz_beschreibung"
FROM "statistics-austria-ogdext-klassdb-oenace2008-1"
