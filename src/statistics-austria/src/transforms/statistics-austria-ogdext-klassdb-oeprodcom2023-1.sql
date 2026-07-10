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
    "nationale_position",
    "korrespondierender_code",
    "korrespondierender_titel",
    "ma_einheit2",
    "korrespondierender_edv_code",
    "ma_einheit",
    "kurztitel",
    "titel",
    "korrespondierende_ebene",
    "korrespondenz_beschreibung"
FROM "statistics-austria-ogdext-klassdb-oeprodcom2023-1"
