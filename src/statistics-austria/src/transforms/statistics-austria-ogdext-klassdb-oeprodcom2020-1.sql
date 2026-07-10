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
    "ma_einheit",
    "korrespondierende_ebene",
    "ma_einheit2",
    "liste_oeprodcom",
    "nationale_position",
    "korrespondierender_edv_code",
    "korrespondierender_titel",
    "korrespondenz_beschreibung",
    "titel",
    "kurztitel",
    "korrespondierender_code"
FROM "statistics-austria-ogdext-klassdb-oeprodcom2020-1"
