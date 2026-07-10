-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    "REFNIS" AS refnis,
    "REFNIS_NL" AS refnis_nl,
    "REFNIS_FR" AS refnis_fr,
    CAST("CD_YEAR" AS BIGINT) AS cd_year,
    CAST("CD_PERIOD" AS BIGINT) AS cd_period,
    "MS_BUILDING_RES_NEW" AS ms_building_res_new,
    "MS_DWELLING_RES_NEW" AS ms_dwelling_res_new,
    "MS_APARTMENT_RES_NEW" AS ms_apartment_res_new,
    "MS_SINGLE_HOUSE_RES_NEW" AS ms_single_house_res_new,
    "MS_TOTAL_SURFACE_RES_NEW" AS ms_total_surface_res_new,
    "MS_BUILDING_RES_RENOVATION" AS ms_building_res_renovation,
    "MS_BUILDING_NONRES_NEW" AS ms_building_nonres_new,
    "MS_VOLUME_NONRES_NEW" AS ms_volume_nonres_new,
    "MS_BUILDING_NONRES_RENOVATION" AS ms_building_nonres_renovation,
    "CD_REFNIS_NATION" AS cd_refnis_nation,
    "CD_REFNIS_REGION" AS cd_refnis_region,
    "CD_REFNIS_PROVINCE" AS cd_refnis_province,
    "CD_REFNIS_DISTRICT" AS cd_refnis_district,
    "CD_REFNIS_MUNICIPALITY" AS cd_refnis_municipality,
    CAST("CD_REFNIS_LEVEL" AS BIGINT) AS cd_refnis_level
FROM "statbel-nodeid3461"
