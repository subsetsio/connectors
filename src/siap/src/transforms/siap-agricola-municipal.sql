-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are denormalized observations with geography, crop, cycle, modality, and unit labels repeated on each row; the source contains duplicate observation rows, so `source_row_number` is part of the row identity.
SELECT
    "source_row_number",
    "source_year",
    "anio",
    CAST("idestado" AS BIGINT) AS idestado,
    "nomestado",
    CAST("idddr" AS BIGINT) AS idddr,
    "nomddr",
    CAST("idcader" AS BIGINT) AS idcader,
    "nomcader",
    CAST("idmunicipio" AS BIGINT) AS idmunicipio,
    "nommunicipio",
    CAST("idciclo" AS BIGINT) AS idciclo,
    "nomcicloproductivo",
    CAST("idmodalidad" AS BIGINT) AS idmodalidad,
    "nommodalidad",
    CAST("idunidadmedida" AS BIGINT) AS idunidadmedida,
    "nomunidad",
    CAST("idcultivo" AS BIGINT) AS idcultivo,
    "nomcultivo",
    "sembrada",
    "cosechada",
    "siniestrada",
    "volumenproduccion",
    "rendimiento",
    "precio",
    "valorproduccion"
FROM "siap-agricola-municipal"
