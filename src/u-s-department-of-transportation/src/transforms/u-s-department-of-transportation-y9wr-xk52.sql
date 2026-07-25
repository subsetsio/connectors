-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("shipmt_id" AS BIGINT) AS shipmt_id,
    CAST("orig_state" AS BIGINT) AS orig_state,
    CAST("orig_ma" AS BIGINT) AS orig_ma,
    "orig_cfs_area",
    CAST("dest_state" AS BIGINT) AS dest_state,
    CAST("dest_ma" AS BIGINT) AS dest_ma,
    "dest_cfs_area",
    CAST("naics" AS BIGINT) AS naics,
    CAST("quarter" AS BIGINT) AS quarter,
    "sctg",
    CAST("mode" AS BIGINT) AS mode,
    CAST("shipmt_value" AS BIGINT) AS shipmt_value,
    CAST("shipmt_wght" AS BIGINT) AS shipmt_wght,
    CAST("shipmt_dist_gc" AS BIGINT) AS shipmt_dist_gc,
    CAST("shipmt_dist_routed" AS BIGINT) AS shipmt_dist_routed,
    CAST("temp_cntl_yn" AS BOOLEAN) AS temp_cntl_yn,
    CAST("export_yn" AS BOOLEAN) AS export_yn,
    "export_cntry",
    "hazmat",
    CAST("wgt_factor" AS DOUBLE) AS wgt_factor
FROM "u-s-department-of-transportation-y9wr-xk52"
