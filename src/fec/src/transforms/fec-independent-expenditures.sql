-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Independent expenditures are spending for or against a candidate and are not contributions to that candidate; aggregate support and opposition separately.
SELECT
    CAST("cycle" AS BIGINT) AS cycle,
    "cand_id",
    "cand_name",
    "spe_id",
    "spe_nam",
    "ele_type",
    "can_office_state",
    "can_office_dis",
    "can_office",
    "cand_pty_aff",
    CAST("exp_amo" AS BIGINT) AS exp_amo,
    strptime("exp_date", '%m/%d/%Y')::DATE AS exp_date,
    CAST("agg_amo" AS DOUBLE) AS agg_amo,
    "sup_opp",
    "pur",
    "pay",
    CAST("file_num" AS BIGINT) AS file_num,
    "amndt_ind",
    "tran_id",
    CAST("image_num" AS BIGINT) AS image_num,
    strptime("receipt_dat", '%m/%d/%Y')::DATE AS receipt_dat,
    CAST("fec_election_yr" AS BIGINT) AS fec_election_yr,
    CAST("prev_file_num" AS BIGINT) AS prev_file_num,
    strptime("dissem_dt", '%m/%d/%Y')::DATE AS dissem_dt
FROM "fec-independent-expenditures"
