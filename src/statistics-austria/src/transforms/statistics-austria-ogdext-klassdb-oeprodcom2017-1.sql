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
    "liste_oeprodcom",
    "ma_einheit2",
    "korrespondierender_edv_code",
    "korrespondierender_code",
    "kurztitel",
    "titel",
    "nationale_position",
    "korrespondierende_ebene",
    "korrespondierender_titel",
    "korrespondenz_beschreibung",
    "ma_einheit"
FROM "statistics-austria-ogdext-klassdb-oeprodcom2017-1"
