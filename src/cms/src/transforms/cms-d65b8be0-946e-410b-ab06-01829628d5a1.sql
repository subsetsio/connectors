-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "PROVNUM" AS provnum,
    "STATE" AS state,
    "CY_Qtr" AS cy_qtr,
    strptime("WorkDate", '%Y%m%d')::DATE AS workdate,
    CAST("SYS_EMPLEE_ID" AS BIGINT) AS sys_emplee_id,
    CAST("EMPLEE_JOB_CD_ID" AS BIGINT) AS emplee_job_cd_id,
    CAST("EMP_CTR" AS BIGINT) AS emp_ctr,
    "WORK_HRS_NUM" AS work_hrs_num,
    "WORK_HRS_FN" AS work_hrs_fn
FROM "cms-d65b8be0-946e-410b-ab06-01829628d5a1"
