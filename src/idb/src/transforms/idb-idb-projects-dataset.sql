-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "oper_num",
    "oper_nm",
    CAST("apprvl_dt" AS TIMESTAMP) AS apprvl_dt,
    CAST("sign_dt" AS TIMESTAMP) AS sign_dt,
    "cntry_cd",
    "cntry_nm",
    "publc_sts_nm",
    "sector_cd",
    "sector_nm",
    "subsector_cd",
    "subsector_nm",
    "oper_typ_cd",
    "opertyp_nm",
    "objtv",
    CAST("orig_apprvd_useq_amnt" AS DOUBLE) AS orig_apprvd_useq_amnt,
    CAST("totl_cost_orig" AS BIGINT) AS totl_cost_orig,
    CAST("loc_cntrprt" AS BIGINT) AS loc_cntrprt,
    "lending_typ_nm",
    "modality_cd",
    "modality_nm",
    "facility_typ_cd",
    "facility_typ_nm",
    "envmntl_clssfctn_cd",
    "envmntl_clssfctn_nm",
    "lending_instrmnt_cd",
    "lending_instrmnt_nm",
    "lending_typ_cd",
    "sts_cd",
    "source_resource"
FROM "idb-idb-projects-dataset"
