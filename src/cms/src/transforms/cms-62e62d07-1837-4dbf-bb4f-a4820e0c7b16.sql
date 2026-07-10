-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    "YEAR_TYPE" AS year_type,
    "SMRY_CTGRY" AS smry_ctgry,
    "SRVC_CTGRY" AS srvc_ctgry,
    "PRVDR_ID" AS prvdr_id,
    "PRVDR_NAME" AS prvdr_name,
    "PRVDR_CITY" AS prvdr_city,
    "STATE" AS state,
    "PRVDR_ZIP" AS prvdr_zip,
    CAST("GRPNG" AS BIGINT) AS grpng,
    "GRPNG_DESC" AS grpng_desc,
    CAST("BENE_DSTNCT_CNT" AS BIGINT) AS bene_dstnct_cnt,
    CAST("TOT_EPSD_STAY_CNT" AS BIGINT) AS tot_epsd_stay_cnt,
    CAST("TOT_SRVC_DAYS" AS BIGINT) AS tot_srvc_days,
    CAST("AVG_CHRG_PER_BENE" AS BIGINT) AS avg_chrg_per_bene,
    CAST("AVG_ALOWD_AMT_PER_BENE" AS BIGINT) AS avg_alowd_amt_per_bene,
    CAST("AVG_PYMT_AMT_PER_BENE" AS BIGINT) AS avg_pymt_amt_per_bene,
    CAST("AVG_STDZD_PYMT_AMT_PER_BENE" AS BIGINT) AS avg_stdzd_pymt_amt_per_bene,
    CAST("AVG_CHRG_PER_STAY" AS BIGINT) AS avg_chrg_per_stay,
    CAST("AVG_ALOWD_AMT_PER_STAY" AS BIGINT) AS avg_alowd_amt_per_stay,
    CAST("AVG_PYMT_AMT_PER_STAY" AS BIGINT) AS avg_pymt_amt_per_stay,
    CAST("AVG_STDZD_PYMT_AMT_PER_STAY" AS BIGINT) AS avg_stdzd_pymt_amt_per_stay,
    CAST("AVG_CHRG_PER_DAY" AS BIGINT) AS avg_chrg_per_day,
    CAST("AVG_ALOWD_AMT_PER_DAY" AS BIGINT) AS avg_alowd_amt_per_day,
    CAST("AVG_PYMT_AMT_PER_DAY" AS BIGINT) AS avg_pymt_amt_per_day,
    CAST("AVG_STDZD_PYMT_AMT_PER_DAY" AS BIGINT) AS avg_stdzd_pymt_amt_per_day,
    "CASEMIX" AS casemix,
    "CASEMIX_DAY_PCT" AS casemix_day_pct
FROM "cms-62e62d07-1837-4dbf-bb4f-a4820e0c7b16"
