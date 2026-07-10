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
    "korrespondierender_code",
    "kurztitel",
    "ma_einheit2",
    "korrespondierender_edv_code",
    "liste_oeprodcom",
    "nationale_position",
    "ma_einheit",
    "korrespondenz_beschreibung",
    "korrespondierende_ebene",
    "korrespondierender_titel",
    "titel"
FROM "statistics-austria-ogdext-klassdb-oeprodcom2022-1"
