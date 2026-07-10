-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    CAST("LVL_NACEBEL" AS BIGINT) AS lvl_nacebel,
    "CD_NACEBEL" AS cd_nacebel,
    "CD_SUP_NACEBEL" AS cd_sup_nacebel,
    "TX_NACEBEL_DE" AS tx_nacebel_de,
    "TX_NACEBEL_EN" AS tx_nacebel_en,
    "TX_NACEBEL_FR" AS tx_nacebel_fr,
    "TX_NACEBEL_NL" AS tx_nacebel_nl,
    "DT_VLDT_START" AS dt_vldt_start,
    strptime("DT_VLDT_END", '%d/%m/%Y')::DATE AS dt_vldt_end
FROM "statbel-nodeid740"
