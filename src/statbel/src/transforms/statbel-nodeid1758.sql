-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    "CD_STAT_SECTOR" AS cd_stat_sector,
    CAST("CD_YEAR" AS BIGINT) AS cd_year,
    "CD_TYPE" AS cd_type,
    "CD_TYPE_NL" AS cd_type_nl,
    "CD_TYPE_FR" AS cd_type_fr,
    CAST("MS_TRANSACTIONS" AS BIGINT) AS ms_transactions,
    "MS_P25" AS ms_p25,
    "MS_P50__MEDIAN_PRICE" AS ms_p50_median_price,
    "MS_P75" AS ms_p75,
    "MS_P10" AS ms_p10,
    "MS_P90" AS ms_p90
FROM "statbel-nodeid1758"
