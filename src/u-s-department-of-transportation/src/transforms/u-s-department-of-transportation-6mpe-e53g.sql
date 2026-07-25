-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("carprocessgrp" AS BIGINT) AS carprocessgrp,
    "period_type",
    CAST("year" AS BIGINT) AS year,
    CAST("quarter" AS BIGINT) AS quarter,
    CAST("group_sort" AS BIGINT) AS group_sort,
    "group_name",
    CAST("airlineid" AS BIGINT) AS airlineid,
    "uniquecarrier",
    "uniquecarriername",
    CAST("item_id" AS BIGINT) AS item_id,
    "item_name",
    CAST("val" AS DOUBLE) AS val,
    "pk"
FROM "u-s-department-of-transportation-6mpe-e53g"
