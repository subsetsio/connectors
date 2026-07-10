-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    CAST("CD_YEAR" AS BIGINT) AS cd_year,
    "CD_TYPE_NL" AS cd_type_nl,
    "CD_TYPE_FR" AS cd_type_fr,
    CAST("CD_REFNIS" AS BIGINT) AS cd_refnis,
    "CD_REFNIS_NL" AS cd_refnis_nl,
    "CD_REFNIS_FR" AS cd_refnis_fr,
    "CD_PERIOD" AS cd_period,
    "CD_CLASS_SURFACE" AS cd_class_surface,
    CAST("MS_TOTAL_TRANSACTIONS" AS BIGINT) AS ms_total_transactions,
    "MS_TOTAL_PRICE" AS ms_total_price,
    "MS_TOTAL_SURFACE" AS ms_total_surface,
    "MS_MEAN_PRICE" AS ms_mean_price,
    "MS_P10" AS ms_p10,
    "MS_P25" AS ms_p25,
    "MS_P50" AS ms_p50,
    "MS_P75" AS ms_p75,
    "MS_P90" AS ms_p90
FROM "statbel-nodeid678"
