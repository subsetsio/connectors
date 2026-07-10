-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    "DT_DAY" AS dt_day,
    CAST("DT_HOUR" AS BIGINT) AS dt_hour,
    CAST("CD_DAY_OF_WEEK" AS BIGINT) AS cd_day_of_week,
    "TX_DAY_OF_WEEK_DESCR_FR" AS tx_day_of_week_descr_fr,
    "TX_DAY_OF_WEEK_DESCR_NL" AS tx_day_of_week_descr_nl,
    "CD_BUILD_UP_AREA" AS cd_build_up_area,
    "TX_BUILD_UP_AREA_DESCR_NL" AS tx_build_up_area_descr_nl,
    "TX_BUILD_UP_AREA_DESCR_FR" AS tx_build_up_area_descr_fr,
    "CD_COLL_TYPE" AS cd_coll_type,
    "TX_COLL_TYPE_DESCR_NL" AS tx_coll_type_descr_nl,
    "TX_COLL_TYPE_DESCR_FR" AS tx_coll_type_descr_fr,
    "CD_LIGHT_COND" AS cd_light_cond,
    "TX_LIGHT_COND_DESCR_NL" AS tx_light_cond_descr_nl,
    "TX_LIGHT_COND_DESCR_FR" AS tx_light_cond_descr_fr,
    "CD_ROAD_TYPE" AS cd_road_type,
    "TX_ROAD_TYPE_DESCR_NL" AS tx_road_type_descr_nl,
    "TX_ROAD_TYPE_DESCR_FR" AS tx_road_type_descr_fr,
    CAST("CD_MUNTY_REFNIS" AS BIGINT) AS cd_munty_refnis,
    "TX_MUNTY_DESCR_NL" AS tx_munty_descr_nl,
    "TX_MUNTY_DESCR_FR" AS tx_munty_descr_fr,
    CAST("CD_DSTR_REFNIS" AS BIGINT) AS cd_dstr_refnis,
    "TX_ADM_DSTR_DESCR_NL" AS tx_adm_dstr_descr_nl,
    "TX_ADM_DSTR_DESCR_FR" AS tx_adm_dstr_descr_fr,
    "CD_PROV_REFNIS" AS cd_prov_refnis,
    "TX_PROV_DESCR_NL" AS tx_prov_descr_nl,
    "TX_PROV_DESCR_FR" AS tx_prov_descr_fr,
    "CD_RGN_REFNIS" AS cd_rgn_refnis,
    "TX_RGN_DESCR_NL" AS tx_rgn_descr_nl,
    "TX_RGN_DESCR_FR" AS tx_rgn_descr_fr,
    CAST("MS_ACCT" AS BIGINT) AS ms_acct,
    CAST("MS_ACCT_WITH_DEAD" AS BIGINT) AS ms_acct_with_dead,
    CAST("MS_ACCT_WITH_DEAD_30_DAYS" AS BIGINT) AS ms_acct_with_dead_30_days,
    CAST("MS_ACCT_WITH_MORY_INJ" AS BIGINT) AS ms_acct_with_mory_inj,
    CAST("MS_ACCT_WITH_SERLY_INJ" AS BIGINT) AS ms_acct_with_serly_inj,
    CAST("MS_ACCT_WITH_SLY_INJ" AS BIGINT) AS ms_acct_with_sly_inj
FROM "statbel-nodeid2118"
