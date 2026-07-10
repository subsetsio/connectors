-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("CD_REFNIS" AS BIGINT) AS cd_refnis,
    "TX_MUNTY_DESCR_FR" AS tx_munty_descr_fr,
    "TX_MUNTY_DESCR_NL" AS tx_munty_descr_nl,
    "TX_FST_NAME" AS tx_fst_name,
    CAST("MS_FREQUENCY" AS BIGINT) AS ms_frequency
FROM "statbel-nodeid1573"
