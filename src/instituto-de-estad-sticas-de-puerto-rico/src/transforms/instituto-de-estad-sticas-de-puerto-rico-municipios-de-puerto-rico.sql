-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    CAST("cuerdas" AS DOUBLE) AS cuerdas,
    strptime("date_date", '%Y%m%d')::DATE AS date_date,
    "time_date",
    "countyfp",
    CAST("fid" AS DOUBLE) AS fid,
    CAST("area" AS DOUBLE) AS area,
    CAST("shape_area" AS DOUBLE) AS shape_area,
    "municipio",
    CAST("shape_leng" AS DOUBLE) AS shape_leng,
    CAST("cntyidfp" AS BIGINT) AS cntyidfp,
    CAST("statefp" AS BIGINT) AS statefp
FROM "instituto-de-estad-sticas-de-puerto-rico-municipios-de-puerto-rico"
