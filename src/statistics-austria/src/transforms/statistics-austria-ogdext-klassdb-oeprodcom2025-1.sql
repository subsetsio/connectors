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
    "korrespondierender_titel",
    "korrespondierender_code",
    "unit_of_measurement_2",
    "unit_of_measurement",
    "ma_einheit",
    "nationale_position",
    "korrespondenz_beschreibung",
    "ma_einheit2",
    "titel",
    "korrespondierende_ebene",
    "oeprodcom_list",
    "korrespondierender_edv_code",
    "kurztitel",
    "liste_oeprodcom",
    "national_position"
FROM "statistics-austria-ogdext-klassdb-oeprodcom2025-1"
