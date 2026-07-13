-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "CUSTOMID" AS customid,
    "FAC_cone_classification" AS fac_cone_classification,
    "MRR_DATE" AS mrr_date,
    CAST("MRR_INTERVW_ID1" AS BIGINT) AS mrr_intervw_id1,
    CAST("MRR_INTERVW_ID2" AS BIGINT) AS mrr_intervw_id2,
    "MRR_CHILD_BIRTHDATE" AS mrr_child_birthdate,
    "MRR_CHILD_BIRTHDATE_DATE" AS mrr_child_birthdate_date,
    "MRR_CHILD_ENROLLMENT" AS mrr_child_enrollment,
    "MRR_CHILD_ENROLLMENT_DATE" AS mrr_child_enrollment_date,
    "MRR_CHILD_SERVICES" AS mrr_child_services,
    "MRR_CHILD_SERVICES_AGE" AS mrr_child_services_age,
    CAST("FAC_TYPE" AS BIGINT) AS fac_type,
    CAST("age" AS BIGINT) AS age,
    CAST("TODAY_DAY" AS BIGINT) AS today_day,
    "TODAY_MON" AS today_mon,
    CAST("TODAY_YR" AS BIGINT) AS today_yr,
    "compl",
    "module",
    CAST("RECORD_ID" AS BIGINT) AS record_id,
    "dist_num",
    "dist_name",
    "arm",
    "iso",
    CAST("FACILITY_ID2" AS BIGINT) AS facility_id2,
    "source_resource"
FROM "idb-baseline-salud-mesoamrica-belize-health-facility-survey-2015"
