SELECT
    cycle,
    LINKAGE_ID                                AS linkage_id,
    CAND_ID                                   AS cand_id,
    CMTE_ID                                   AS cmte_id,
    CMTE_TP                                   AS cmte_type,
    CMTE_DSGN                                 AS cmte_designation,
    TRY_CAST(CAND_ELECTION_YR AS INTEGER)     AS cand_election_yr,
    TRY_CAST(FEC_ELECTION_YR AS INTEGER)      AS fec_election_yr
FROM "fec-candidate-committee-linkages"
WHERE LINKAGE_ID IS NOT NULL AND LINKAGE_ID <> ''
QUALIFY row_number() OVER (
    PARTITION BY cycle, LINKAGE_ID ORDER BY CMTE_ID
) = 1
