-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    CAST("LVL_ISCO08_KEYWORDS" AS BIGINT) AS lvl_isco08_keywords,
    "CD_ISCO08_KEYWORDS" AS cd_isco08_keywords,
    "CD_SUP_ISCO08_KEYWORDS" AS cd_sup_isco08_keywords,
    "TX_ISCO08_KEYWORDS_DE" AS tx_isco08_keywords_de,
    "TX_ISCO08_KEYWORDS_EN" AS tx_isco08_keywords_en,
    "TX_ISCO08_KEYWORDS_FR" AS tx_isco08_keywords_fr,
    "TX_ISCO08_KEYWORDS_NL" AS tx_isco08_keywords_nl,
    "DT_VLDT_START" AS dt_vldt_start,
    strptime("DT_VLDT_END", '%d/%m/%Y')::DATE AS dt_vldt_end
FROM "statbel-nodeid735"
