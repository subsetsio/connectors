-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "AGG_ID" AS agg_id,
    CAST("HRR_NUM_MY" AS BIGINT) AS hrr_num_my,
    "HDR_MY" AS hdr_my,
    "HDR_DNM_MY" AS hdr_dnm_my,
    "HDR_NUM_MY" AS hdr_num_my,
    "HD_NUM_MY" AS hd_num_my,
    "SD_NUM_MY" AS sd_num_my,
    "NOCD_NUM_MY" AS nocd_num_my,
    "TR_MY_ACHSCR" AS tr_my_achscr,
    "TR_MY_IMPSCR" AS tr_my_impscr,
    "TWR_DNM_MY" AS twr_dnm_my,
    "TWR_NUM_MY" AS twr_num_my,
    "LDT_DNM_MY" AS ldt_dnm_my,
    "LDT_NUM_MY" AS ldt_num_my,
    "BENECNT_LDT_MY" AS benecnt_ldt_my,
    "HEI_HDR" AS hei_hdr,
    "HDR_DELIS_DIFF" AS hdr_delis_diff,
    "HDR_DELIS_MY" AS hdr_delis_my,
    "HDR_DNM_DELIS_MY" AS hdr_dnm_delis_my,
    "HDR_NUM_DELIS_MY" AS hdr_num_delis_my,
    "HEI_TR" AS hei_tr,
    "TR_DELIS_DIFF" AS tr_delis_diff,
    "TR_DELIS_MY" AS tr_delis_my,
    "TWR_DNM_DELIS_MY" AS twr_dnm_delis_my,
    "TWR_NUM_DELIS_MY" AS twr_num_delis_my,
    "LDT_DNM_DELIS_MY" AS ldt_dnm_delis_my,
    "LDT_NUM_DELIS_MY" AS ldt_num_delis_my,
    "MPS" AS mps,
    "PPA" AS ppa,
    CAST("PPA_PERIOD" AS BIGINT) AS ppa_period,
    CAST("MY" AS BIGINT) AS my
FROM "cms-4bae4223-a1dc-4b9c-bd7e-d9622461be35"
