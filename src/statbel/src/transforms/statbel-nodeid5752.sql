-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    CAST("LVL_REFNIS" AS BIGINT) AS lvl_refnis,
    "CD_REFNIS" AS cd_refnis,
    "CD_SUP_REFNIS" AS cd_sup_refnis,
    "TX_REFNIS_DE" AS tx_refnis_de,
    "TX_REFNIS_FR" AS tx_refnis_fr,
    "TX_REFNIS_NL" AS tx_refnis_nl,
    "DT_VLDT_START" AS dt_vldt_start,
    strptime("DT_VLDT_END", '%d/%m/%Y')::DATE AS dt_vldt_end
FROM "statbel-nodeid5752"
