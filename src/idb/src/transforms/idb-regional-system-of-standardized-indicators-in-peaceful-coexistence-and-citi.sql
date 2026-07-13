-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PAIS" AS pais,
    "DELITO" AS delito,
    "VAR" AS var,
    CAST("POBLACION" AS BIGINT) AS poblacion,
    CAST("ANO" AS BIGINT) AS ano,
    CAST("ANO_Date" AS BIGINT) AS ano_date,
    CAST("NUM" AS DOUBLE) AS num,
    "LOCATION" AS location,
    "source_resource"
FROM "idb-regional-system-of-standardized-indicators-in-peaceful-coexistence-and-citi"
