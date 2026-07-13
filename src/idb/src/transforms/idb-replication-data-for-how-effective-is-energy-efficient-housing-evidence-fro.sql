-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Fecha" AS fecha,
    CAST("hour" AS BIGINT) AS hour,
    CAST("Folio_SIMO" AS BIGINT) AS folio_simo,
    CAST("LecturasHR" AS DOUBLE) AS lecturashr,
    CAST("LecturasC" AS DOUBLE) AS lecturasc,
    "source_resource"
FROM "idb-replication-data-for-how-effective-is-energy-efficient-housing-evidence-fro"
