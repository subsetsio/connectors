SELECT
    cycle,
    CAND_ID                                       AS cand_id,
    CAND_NAME                                     AS cand_name,
    CAND_PTY_AFFILIATION                          AS party,
    CASE CN_OFFICE WHEN 'H' THEN 'House' WHEN 'S' THEN 'Senate' WHEN 'P' THEN 'President' ELSE CN_OFFICE END                                AS office,
    CAND_OFFICE_ST                                AS state,
    CAND_OFFICE_DISTRICT                          AS district,
    CASE CAND_ICI WHEN 'I' THEN 'Incumbent' WHEN 'C' THEN 'Challenger' WHEN 'O' THEN 'Open Seat' ELSE CAND_ICI END                                   AS incumbent_challenger,
    CN_PCC                                        AS principal_cmte_id,
    TRY_CAST(TTL_RECEIPTS AS DOUBLE)              AS total_receipts,
    TRY_CAST(TTL_DISB AS DOUBLE)                  AS total_disbursements,
    TRY_CAST(TTL_INDIV_CONTRIB AS DOUBLE)         AS total_individual_contrib,
    TRY_CAST(OTHER_POL_CMTE_CONTRIB AS DOUBLE)    AS other_cmte_contrib,
    TRY_CAST(POL_PTY_CONTRIB AS DOUBLE)           AS party_contrib,
    TRY_CAST(CAND_CONTRIB AS DOUBLE)              AS cand_contributions,
    TRY_CAST(CAND_LOANS AS DOUBLE)               AS cand_loans,
    TRY_CAST(COH_COP AS DOUBLE)                   AS cash_on_hand_end,
    TRY_CAST(DEBTS_OWED_BY AS DOUBLE)             AS debts_owed_by,
    TRY_STRPTIME(CVG_END_DT, '%m/%d/%Y')::DATE    AS coverage_end_date
FROM "fec-candidates"
WHERE CAND_ID IS NOT NULL AND CAND_ID <> ''
QUALIFY row_number() OVER (
    PARTITION BY cycle, CAND_ID
    ORDER BY TRY_CAST(TTL_RECEIPTS AS DOUBLE) DESC NULLS LAST
) = 1
