-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Monthly CES observations mix geographic areas and employment series; filter both `area` and `series` before trend analysis.
SELECT
    "area",
    "area_name",
    "series",
    "title",
    CAST("year" AS BIGINT) AS year,
    CAST("month" AS BIGINT) AS month,
    CAST("current_employment" AS BIGINT) AS current_employment
FROM "new-york-state-department-of-labor-6k74-dgkb"
