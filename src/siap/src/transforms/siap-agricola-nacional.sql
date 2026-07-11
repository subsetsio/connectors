-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a frozen historical national-schema series ending in 2002; current agricultural observations are published in the municipal-schema table.
SELECT
    "source_year",
    "anio",
    CAST("idestado" AS BIGINT) AS idestado,
    "nomestado",
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
FROM "siap-agricola-nacional"
