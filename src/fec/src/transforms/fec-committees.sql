-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Committee summaries include multiple committee types, including candidate committees, party committees, PACs, and independent-expenditure-only committees; filter committee type before comparing totals across committee classes.
SELECT
    CAST("cycle" AS BIGINT) AS cycle,
    "CMTE_ID" AS cmte_id,
    "CMTE_NM" AS cmte_nm,
    "CMTE_TP" AS cmte_tp,
    "CMTE_DSGN" AS cmte_dsgn,
    "CMTE_FILING_FREQ" AS cmte_filing_freq,
    CAST("TTL_RECEIPTS" AS BIGINT) AS ttl_receipts,
    CAST("TRANS_FROM_AFF" AS BIGINT) AS trans_from_aff,
    CAST("INDV_CONTRIB" AS BIGINT) AS indv_contrib,
    CAST("OTHER_POL_CMTE_CONTRIB" AS BIGINT) AS other_pol_cmte_contrib,
    CAST("CAND_CONTRIB" AS BIGINT) AS cand_contrib,
    CAST("CAND_LOANS" AS BIGINT) AS cand_loans,
    CAST("TTL_LOANS_RECEIVED" AS BIGINT) AS ttl_loans_received,
    CAST("TTL_DISB" AS DOUBLE) AS ttl_disb,
    CAST("TRANF_TO_AFF" AS BIGINT) AS tranf_to_aff,
    CAST("INDV_REFUNDS" AS BIGINT) AS indv_refunds,
    CAST("OTHER_POL_CMTE_REFUNDS" AS BIGINT) AS other_pol_cmte_refunds,
    CAST("CAND_LOAN_REPAY" AS DOUBLE) AS cand_loan_repay,
    CAST("LOAN_REPAY" AS BIGINT) AS loan_repay,
    CAST("COH_BOP" AS DOUBLE) AS coh_bop,
    CAST("COH_COP" AS DOUBLE) AS coh_cop,
    CAST("DEBTS_OWED_BY" AS BIGINT) AS debts_owed_by,
    CAST("NONFED_TRANS_RECEIVED" AS DOUBLE) AS nonfed_trans_received,
    CAST("CONTRIB_TO_OTHER_CMTE" AS BIGINT) AS contrib_to_other_cmte,
    CAST("IND_EXP" AS DOUBLE) AS ind_exp,
    CAST("PTY_COORD_EXP" AS DOUBLE) AS pty_coord_exp,
    "NONFED_SHARE_EXP" AS nonfed_share_exp,
    strptime("CVG_END_DT", '%m/%d/%Y')::DATE AS cvg_end_dt,
    "CM_PTY" AS cm_pty,
    "CM_ST" AS cm_st,
    "CM_ORG_TP" AS cm_org_tp,
    "CM_CONNECTED_ORG" AS cm_connected_org,
    "CM_CAND_ID" AS cm_cand_id
FROM "fec-committees"
