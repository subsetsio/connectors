-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `state` includes the All-India aggregate alongside the states; `sector` includes 'Combined' alongside Rural and Urban; `group`/`subgroup` include 'General' / total rows. Filter before summing.
-- caution: Two base-year series (`baseyear`) coexist and their index levels are not comparable.
-- caution: `status` marks provisional vs final observations.
SELECT
    CAST("baseyear" AS BIGINT) AS baseyear,
    CAST("year" AS BIGINT) AS year,
    "month",
    "state",
    "sector",
    "group",
    "subgroup",
    CAST("index" AS DOUBLE) AS index,
    CAST("inflation" AS DOUBLE) AS inflation,
    "status"
FROM "mospi-cpi-getcpiindex"
