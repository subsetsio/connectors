-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "isocode",
    "country",
    CAST("year" AS BIGINT) AS year,
    CAST("Y" AS BIGINT) AS y,
    CAST("K" AS BIGINT) AS k,
    CAST("Lpop" AS DOUBLE) AS lpop,
    CAST("Lemp" AS DOUBLE) AS lemp,
    CAST("S" AS DOUBLE) AS s,
    CAST("h" AS DOUBLE) AS h,
    "alpha_it",
    "a",
    CAST("LP" AS DOUBLE) AS lp,
    CAST("KLP" AS DOUBLE) AS klp,
    CAST("TFP" AS DOUBLE) AS tfp,
    CAST("LAC" AS BIGINT) AS lac,
    CAST("ROW" AS BIGINT) AS row,
    CAST("DEV" AS BIGINT) AS dev,
    CAST("EA" AS BIGINT) AS ea,
    CAST("Twin" AS BIGINT) AS twin,
    "source_resource"
FROM "idb-productivity-and-factor-accumulation-in-latin-america-and-the-caribbean-a-d"
