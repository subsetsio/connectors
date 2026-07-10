-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Month" AS month,
    CAST("Sort" AS BIGINT) AS sort,
    CAST("Year" AS BIGINT) AS year,
    CAST("Page Views" AS BIGINT) AS page_views,
    "Page Visits" AS page_visits
FROM "cdc-rq85-buyi"
