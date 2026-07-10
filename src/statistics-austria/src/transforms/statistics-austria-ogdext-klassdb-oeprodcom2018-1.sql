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
    "nationale_position",
    "liste_oeprodcom",
    "ma_einheit",
    "titel",
    "korrespondierender_code",
    "korrespondenz_beschreibung",
    "ma_einheit2",
    "korrespondierende_ebene",
    "kurztitel",
    "korrespondierender_edv_code",
    "korrespondierender_titel"
FROM "statistics-austria-ogdext-klassdb-oeprodcom2018-1"
