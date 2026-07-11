-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This per-cycle candidate summary overlaps with the current House/Senate campaign summary table; avoid adding both tables together for the same race and cycle.
SELECT
    CAST("cycle" AS BIGINT) AS cycle,
    "CAND_ID" AS cand_id,
    "CAND_NAME" AS cand_name,
    "CAND_ICI" AS cand_ici,
    CAST("PTY_CD" AS BIGINT) AS pty_cd,
    "CAND_PTY_AFFILIATION" AS cand_pty_affiliation,
    CAST("TTL_RECEIPTS" AS DOUBLE) AS ttl_receipts,
    CAST("TRANS_FROM_AUTH" AS DOUBLE) AS trans_from_auth,
    CAST("TTL_DISB" AS DOUBLE) AS ttl_disb,
    CAST("TRANS_TO_AUTH" AS BIGINT) AS trans_to_auth,
    CAST("COH_BOP" AS DOUBLE) AS coh_bop,
    CAST("COH_COP" AS DOUBLE) AS coh_cop,
    CAST("CAND_CONTRIB" AS BIGINT) AS cand_contrib,
    CAST("CAND_LOANS" AS BIGINT) AS cand_loans,
    CAST("OTHER_LOANS" AS BIGINT) AS other_loans,
    CAST("CAND_LOAN_REPAY" AS BIGINT) AS cand_loan_repay,
    CAST("OTHER_LOAN_REPAY" AS BIGINT) AS other_loan_repay,
    CAST("DEBTS_OWED_BY" AS BIGINT) AS debts_owed_by,
    CAST("TTL_INDIV_CONTRIB" AS DOUBLE) AS ttl_indiv_contrib,
    "CAND_OFFICE_ST" AS cand_office_st,
    "CAND_OFFICE_DISTRICT" AS cand_office_district,
    "SPEC_ELECTION" AS spec_election,
    "PRIM_ELECTION" AS prim_election,
    "RUN_ELECTION" AS run_election,
    "GEN_ELECTION" AS gen_election,
    "GEN_ELECTION_PRECENT" AS gen_election_precent,
    CAST("OTHER_POL_CMTE_CONTRIB" AS BIGINT) AS other_pol_cmte_contrib,
    CAST("POL_PTY_CONTRIB" AS BIGINT) AS pol_pty_contrib,
    strptime("CVG_END_DT", '%m/%d/%Y')::DATE AS cvg_end_dt,
    CAST("INDIV_REFUNDS" AS BIGINT) AS indiv_refunds,
    CAST("CMTE_REFUNDS" AS BIGINT) AS cmte_refunds,
    "CN_OFFICE" AS cn_office,
    "CN_PCC" AS cn_pcc
FROM "fec-candidates"
