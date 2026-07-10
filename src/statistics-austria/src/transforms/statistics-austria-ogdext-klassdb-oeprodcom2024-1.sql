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
    "korrespondenz_beschreibung",
    "korrespondierender_edv_code",
    "ma_einheit",
    "titel",
    "korrespondierender_titel",
    "kurztitel",
    "ma_einheit2",
    "liste_oeprodcom",
    "korrespondierende_ebene",
    "nationale_position"
FROM "statistics-austria-ogdext-klassdb-oeprodcom2024-1"
