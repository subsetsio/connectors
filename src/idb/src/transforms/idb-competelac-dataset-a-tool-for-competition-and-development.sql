-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "area",
    "iso_code",
    CAST("year" AS BIGINT) AS year,
    "sector_agg",
    "sector",
    "sector_desc",
    "indicator",
    "indicator_desc",
    "sample_threshold",
    CAST("value" AS DOUBLE) AS value,
    CAST("mean" AS DOUBLE) AS mean,
    CAST("sd" AS DOUBLE) AS sd,
    CAST("p1" AS DOUBLE) AS p1,
    CAST("p5" AS DOUBLE) AS p5,
    CAST("p10" AS DOUBLE) AS p10,
    CAST("p25" AS DOUBLE) AS p25,
    CAST("p50" AS DOUBLE) AS p50,
    CAST("p75" AS DOUBLE) AS p75,
    CAST("p90" AS DOUBLE) AS p90,
    CAST("p95" AS DOUBLE) AS p95,
    CAST("p99" AS DOUBLE) AS p99,
    CAST("number_obs" AS BIGINT) AS number_obs,
    CAST("total" AS DOUBLE) AS total,
    "method_estimation",
    "weight_scheme",
    "pf_labor_input",
    "strategy",
    "note",
    "unit",
    "country_region_1",
    "country_name",
    "source_resource"
FROM "idb-competelac-dataset-a-tool-for-competition-and-development"
