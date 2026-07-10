-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    CAST("CD_YEAR" AS BIGINT) AS cd_year,
    "CD_REFNIS" AS cd_refnis,
    "TX_REFNIS_NL" AS tx_refnis_nl,
    "TX_REFNIS_FR" AS tx_refnis_fr,
    CAST("CD_REFNIS_LVL" AS BIGINT) AS cd_refnis_lvl,
    "CD_STAT_TYPE" AS cd_stat_type,
    "TX_STAT_TYPE_NL" AS tx_stat_type_nl,
    "TX_STAT_TYPE_FR" AS tx_stat_type_fr,
    "CD_BUILDING_TYPE" AS cd_building_type,
    "TX_BUILDING_TYPE_NL" AS tx_building_type_nl,
    "TX_BUILDING_TYPE_FR" AS tx_building_type_fr,
    "MS_VALUE" AS ms_value
FROM "statbel-nodeid4129"
