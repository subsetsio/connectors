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
    "name",
    CAST("year_" AS TIMESTAMP) AS year_2,
    CAST("percent_1" AS DOUBLE) AS percent_1,
    CAST("change_from_previous_year_1" AS DOUBLE) AS change_from_previous_year_1,
    "commuting_mode",
    CAST("rank" AS BIGINT) AS rank,
    CAST("date" AS TIMESTAMP) AS date,
    CAST("year_1" AS TIMESTAMP) AS year_1
FROM "u-s-department-of-transportation-pqmc-mnds"
