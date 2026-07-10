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
    "GRPNG" AS grpng,
    "GRPNG_DESC" AS grpng_desc,
    CAST("BENE_DSTNCT_CNT" AS BIGINT) AS bene_dstnct_cnt,
    CAST("TOT_EPSD_STAY_CNT" AS BIGINT) AS tot_epsd_stay_cnt,
    CAST("TOT_SRVC_DAYS" AS BIGINT) AS tot_srvc_days,
    CAST("AVG_CHRG_PER_BENE" AS BIGINT) AS avg_chrg_per_bene,
    CAST("AVG_ALOWD_AMT_PER_BENE" AS BIGINT) AS avg_alowd_amt_per_bene,
    CAST("AVG_PYMT_AMT_PER_BENE" AS BIGINT) AS avg_pymt_amt_per_bene,
    CAST("AVG_STDZD_PYMT_AMT_PER_BENE" AS BIGINT) AS avg_stdzd_pymt_amt_per_bene,
    CAST("AVG_CHRG_PER_EPSD" AS BIGINT) AS avg_chrg_per_epsd,
    CAST("AVG_ALOWD_AMT_PER_EPSD" AS BIGINT) AS avg_alowd_amt_per_epsd,
    CAST("AVG_PYMT_AMT_PER_EPSD" AS BIGINT) AS avg_pymt_amt_per_epsd,
    CAST("AVG_STDZD_PYMT_AMT_PER_EPSD" AS BIGINT) AS avg_stdzd_pymt_amt_per_epsd,
    CAST("AVG_CHRG_PER_DAY" AS BIGINT) AS avg_chrg_per_day,
    CAST("AVG_ALOWD_AMT_PER_DAY" AS BIGINT) AS avg_alowd_amt_per_day,
    CAST("AVG_PYMT_AMT_PER_DAY" AS BIGINT) AS avg_pymt_amt_per_day,
    CAST("AVG_STDZD_PYMT_AMT_PER_DAY" AS BIGINT) AS avg_stdzd_pymt_amt_per_day,
    "PT_VISITS_CNT" AS pt_visits_cnt,
    "OT_VISITS_CNT" AS ot_visits_cnt,
    "SLP_VISITS_CNT" AS slp_visits_cnt,
    "CASEMIX_SRC_TMNG" AS casemix_src_tmng,
    "CASEMIX_SRC_TMNG_EPSD_PCT" AS casemix_src_tmng_epsd_pct,
    "CASEMIX_CMRBDTY" AS casemix_cmrbdty,
    "CASEMIX_CMRBDTY_EPSD_PCT" AS casemix_cmrbdty_epsd_pct
FROM "cms-6c63099b-0794-40a0-925c-51a66b9b9901"
