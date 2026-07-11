-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("UNITID" AS BIGINT) AS unitid,
    CAST("DVADM01" AS BIGINT) AS dvadm01,
    "DVADM02" AS dvadm02,
    "DVADM03" AS dvadm03,
    "DVADM04" AS dvadm04,
    "DVADM05" AS dvadm05,
    "DVADM06" AS dvadm06,
    "DVADM07" AS dvadm07,
    "DVADM08" AS dvadm08,
    "DVADM09" AS dvadm09,
    "DVADM10" AS dvadm10,
    "DVADM11" AS dvadm11,
    "DVADM12" AS dvadm12,
    "year"
FROM "nces-ipeds-drvadm"
