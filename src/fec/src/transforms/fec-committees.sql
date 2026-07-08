SELECT
    cycle,
    CMTE_ID                                       AS cmte_id,
    CMTE_NM                                       AS cmte_name,
    CMTE_TP                                       AS cmte_type,
    CMTE_DSGN                                     AS cmte_designation,
    CM_PTY                                        AS party,
    CM_ST                                         AS state,
    CM_ORG_TP                                     AS org_type,
    CM_CONNECTED_ORG                              AS connected_org,
    CM_CAND_ID                                    AS cand_id,
    TRY_CAST(TTL_RECEIPTS AS DOUBLE)              AS total_receipts,
    TRY_CAST(TTL_DISB AS DOUBLE)                  AS total_disbursements,
    TRY_CAST(INDV_CONTRIB AS DOUBLE)             AS individual_contrib,
    TRY_CAST(OTHER_POL_CMTE_CONTRIB AS DOUBLE)    AS other_cmte_contrib,
    TRY_CAST(CONTRIB_TO_OTHER_CMTE AS DOUBLE)     AS contrib_to_other_cmte,
    TRY_CAST(IND_EXP AS DOUBLE)                   AS independent_expenditures,
    TRY_CAST(PTY_COORD_EXP AS DOUBLE)             AS party_coordinated_exp,
    TRY_CAST(COH_COP AS DOUBLE)                   AS cash_on_hand_end,
    TRY_CAST(DEBTS_OWED_BY AS DOUBLE)             AS debts_owed_by,
    TRY_STRPTIME(CVG_END_DT, '%m/%d/%Y')::DATE    AS coverage_end_date
FROM "fec-committees"
WHERE CMTE_ID IS NOT NULL AND CMTE_ID <> ''
QUALIFY row_number() OVER (
    PARTITION BY cycle, CMTE_ID
    ORDER BY TRY_CAST(TTL_RECEIPTS AS DOUBLE) DESC NULLS LAST
) = 1
