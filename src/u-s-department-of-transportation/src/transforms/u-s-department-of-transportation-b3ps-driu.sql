-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "visualization_id",
    "mode",
    "statistic",
    CAST("year" AS TIMESTAMP) AS year,
    CAST("value" AS DOUBLE) AS value,
    "units",
    CAST("percent" AS DOUBLE) AS percent,
    CAST("fiscal_year" AS TIMESTAMP) AS fiscal_year,
    CAST("change_from_previous_year" AS DOUBLE) AS change_from_previous_year,
    "statistic_short_name"
FROM "u-s-department-of-transportation-b3ps-driu"
