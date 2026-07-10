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
    "CD_REFNIS" AS cd_refnis,
    "CD_REFNIS_NL" AS cd_refnis_nl,
    "CD_REFNIS_FR" AS cd_refnis_fr,
    "CD_PERIOD" AS cd_period,
    "CD_CLASS_SURFACE" AS cd_class_surface,
    "MS_TOTAL_TRANSACTIONS" AS ms_total_transactions,
    "MS_P_25" AS ms_p_25,
    "MS_P_50_median" AS ms_p_50_median,
    "MS_P_75" AS ms_p_75,
    CAST("CD_niveau_refnis" AS BIGINT) AS cd_niveau_refnis
FROM "statbel-nodeid1675"
