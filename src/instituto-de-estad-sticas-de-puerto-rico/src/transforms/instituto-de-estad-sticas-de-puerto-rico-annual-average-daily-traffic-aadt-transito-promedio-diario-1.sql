-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    "PR-" AS pr,
    CAST("KM" AS DOUBLE) AS km,
    "SISTEMA" AS sistema,
    "MUNICIPIO" AS municipio,
    "DESCRIPCIÓN" AS descripci_n,
    CAST("AÑO" AS BIGINT) AS a_o,
    "AADT" AS aadt
FROM "instituto-de-estad-sticas-de-puerto-rico-annual-average-daily-traffic-aadt-transito-promedio-diario-1"
