-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Item-level all-India index; two base-year series (`baseyear`) coexist and are not comparable.
-- caution: `inflation` is null wherever no year-ago observation exists.
SELECT
    CAST("baseyear" AS BIGINT) AS baseyear,
    CAST("year" AS BIGINT) AS year,
    "month",
    "item",
    CAST("index" AS DOUBLE) AS index,
    CAST("inflation" AS DOUBLE) AS inflation,
    "status"
FROM "mospi-cpi-getitemindex"
