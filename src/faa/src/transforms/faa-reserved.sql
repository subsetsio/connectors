-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "N-NUMBER" AS n_number,
    "REGISTRANT" AS registrant,
    "STREET" AS street,
    "STREET2" AS street2,
    "CITY" AS city,
    "STATE" AS state,
    "ZIP CODE" AS zip_code,
    strptime("RSV DATE", '%Y%m%d')::DATE AS rsv_date,
    "TR" AS tr,
    "EXP DATE" AS exp_date,
    "N-NUM-CHG" AS n_num_chg,
    "PURGE DATE" AS purge_date
FROM "faa-reserved"
