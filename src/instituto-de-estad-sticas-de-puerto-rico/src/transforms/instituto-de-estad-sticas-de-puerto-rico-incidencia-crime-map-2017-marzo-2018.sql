-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "Fecha" AS fecha,
    "Hora" AS hora,
    "Delito" AS delito,
    "Delitos_code" AS delitos_code,
    CAST("POINT_X" AS DOUBLE) AS point_x,
    CAST("POINT_Y" AS DOUBLE) AS point_y,
    "Location" AS location,
    "Area Policiaca" AS area_policiaca
FROM "instituto-de-estad-sticas-de-puerto-rico-incidencia-crime-map-2017-marzo-2018"
