-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    CAST("LVL_ISCED_F2013_KEYWORDS" AS BIGINT) AS lvl_isced_f2013_keywords,
    "CD_ISCED_F2013_KEYWORDS" AS cd_isced_f2013_keywords,
    "CD_SUP_ISCED_F2013_KEYWORDS" AS cd_sup_isced_f2013_keywords,
    "TX_ISCED_F2013_KEYWORDS_EN" AS tx_isced_f2013_keywords_en,
    "TX_ISCED_F2013_KEYWORDS_FR" AS tx_isced_f2013_keywords_fr,
    "TX_ISCED_F2013_KEYWORDS_NL" AS tx_isced_f2013_keywords_nl,
    "DT_VLDT_START" AS dt_vldt_start,
    strptime("DT_VLDT_END", '%d/%m/%Y')::DATE AS dt_vldt_end
FROM "statbel-nodeid737"
