-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "origin",
    "dest",
    "sctg",
    "comm",
    "mode",
    CAST("year" AS BIGINT) AS year,
    CAST("val" AS BIGINT) AS val,
    CAST("ton" AS BIGINT) AS ton,
    CAST("tmile" AS BIGINT) AS tmile,
    CAST("avgmile" AS DOUBLE) AS avgmile,
    CAST("val_cv" AS DOUBLE) AS val_cv,
    CAST("ton_cv" AS DOUBLE) AS ton_cv,
    CAST("tmile_cv" AS DOUBLE) AS tmile_cv,
    CAST("avgmile_s" AS DOUBLE) AS avgmile_s
FROM "u-s-department-of-transportation-anet-6eas"
