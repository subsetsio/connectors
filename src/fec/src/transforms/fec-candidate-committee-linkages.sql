-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: A candidate can be linked to multiple committees in the same cycle; filter or group by committee designation before treating a linkage as the candidate's sole campaign committee.
SELECT
    CAST("cycle" AS BIGINT) AS cycle,
    "CAND_ID" AS cand_id,
    CAST("CAND_ELECTION_YR" AS BIGINT) AS cand_election_yr,
    CAST("FEC_ELECTION_YR" AS BIGINT) AS fec_election_yr,
    "CMTE_ID" AS cmte_id,
    "CMTE_TP" AS cmte_tp,
    "CMTE_DSGN" AS cmte_dsgn,
    CAST("LINKAGE_ID" AS BIGINT) AS linkage_id
FROM "fec-candidate-committee-linkages"
