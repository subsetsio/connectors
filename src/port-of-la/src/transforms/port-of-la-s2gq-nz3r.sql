-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source includes duplicate fiscal-year rows, and for some years both partial and fuller rows are present; deduplicate or choose a fiscal-year row deliberately before fiscal-year analysis.
SELECT
    "harbor_department",
    CAST("jul" AS BIGINT) AS jul,
    CAST("aug" AS BIGINT) AS aug,
    CAST("sept" AS BIGINT) AS sept,
    CAST("oct" AS BIGINT) AS oct,
    CAST("nov" AS BIGINT) AS nov,
    CAST("dec" AS BIGINT) AS dec,
    CAST("jan" AS BIGINT) AS jan,
    CAST("feb" AS BIGINT) AS feb,
    CAST("mar" AS BIGINT) AS mar,
    CAST("apr" AS BIGINT) AS apr,
    CAST("may" AS BIGINT) AS may,
    CAST("jun" AS BIGINT) AS jun,
    CAST("total" AS BIGINT) AS total,
    CAST("adjustment" AS BIGINT) AS adjustment,
    CAST("net_total" AS BIGINT) AS net_total
FROM "port-of-la-s2gq-nz3r"
