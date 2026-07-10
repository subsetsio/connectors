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
    "ma_einheit2",
    "liste_oeprodcom",
    "korrespondierende_ebene",
    "titel",
    "nationale_position",
    "korrespondierender_titel",
    "kurztitel",
    "korrespondierender_edv_code",
    "korrespondierender_code",
    "korrespondenz_beschreibung",
    "ma_einheit"
FROM "statistics-austria-ogdext-klassdb-oeprodcom2019-1"
