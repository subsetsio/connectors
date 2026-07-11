-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source includes duplicate fiscal-year rows, and for some years both partial and fuller rows are present; deduplicate or choose a fiscal-year row deliberately before fiscal-year analysis.
SELECT
    "harbor_department",
    CAST("jul" AS DOUBLE) AS jul,
    CAST("aug" AS DOUBLE) AS aug,
    CAST("sep" AS DOUBLE) AS sep,
    CAST("oct" AS DOUBLE) AS oct,
    CAST("nov" AS DOUBLE) AS nov,
    CAST("dec" AS DOUBLE) AS dec,
    CAST("jan" AS DOUBLE) AS jan,
    CAST("feb" AS DOUBLE) AS feb,
    CAST("mar" AS DOUBLE) AS mar,
    CAST("apr" AS DOUBLE) AS apr,
    CAST("may" AS DOUBLE) AS may,
    CAST("jun" AS DOUBLE) AS jun,
    CAST("fy_total" AS DOUBLE) AS fy_total
FROM "port-of-la-v3my-p6u5"
