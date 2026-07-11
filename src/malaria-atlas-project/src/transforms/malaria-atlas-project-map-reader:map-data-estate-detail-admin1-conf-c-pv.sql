-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Confirmed vivax case counts are admin 1 annual values; do not sum them with falciparum or lower-level admin tables without choosing a single geography level.
SELECT
    "id",
    "iso_3_code",
    "iso_2_code",
    CAST("gaul_code" AS BIGINT) AS gaul_code,
    "country_name",
    "admin_level",
    "admin_unit",
    "who_region",
    "who_subregion",
    "world_bank_region",
    CAST("map_pv_relapse_zone" AS BIGINT) AS map_pv_relapse_zone,
    "gender",
    "age_bin",
    "year",
    "api_mean_all",
    "api_mean_pf",
    "api_mean_pv",
    "conf_c",
    "conf_c_pf",
    "conf_c_pv",
    "unconf_c",
    "pf_prop",
    "pv_prop",
    "spr",
    "reporting_compl",
    "total_pop",
    "pop_at_risk_pf",
    "pop_at_risk_pv",
    "pop_at_risk_all",
    "time_start",
    "time_end",
    "_source_type_name" AS source_type_name,
    "_feature_id" AS feature_id,
    "_geometry_name" AS geometry_name,
    "_geometry" AS geometry,
    "_bbox" AS bbox
FROM "malaria-atlas-project-map-reader:map-data-estate-detail-admin1-conf-c-pv"
