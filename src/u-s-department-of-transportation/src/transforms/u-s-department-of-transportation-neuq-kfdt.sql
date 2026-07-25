-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "viz_idx",
    "trans_mode_display",
    "stat_display",
    CAST("year" AS TIMESTAMP) AS year,
    CAST("val" AS DOUBLE) AS val,
    "units",
    CAST("percent" AS DOUBLE) AS percent,
    CAST("fiscal_year" AS TIMESTAMP) AS fiscal_year,
    CAST("_change_from_previous_year" AS DOUBLE) AS change_from_previous_year,
    "statistic_short_name"
FROM "u-s-department-of-transportation-neuq-kfdt"
