-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "feature_id",
    "lat__lat" AS lat_lat,
    "lon__long" AS lon_long,
    "identifier__identifiant" AS identifier_identifiant,
    "station_id__id_station" AS station_id_id_station,
    "period_group__groupe_periode" AS period_group_groupe_periode,
    "period_value__valeur_periode" AS period_value_valeur_periode,
    "province__province" AS province_province,
    "year__annee" AS year_annee,
    "temp_mean__temp_moyenne" AS temp_mean_temp_moyenne,
    "temp_mean_units__temp_moyenne_unites" AS temp_mean_units_temp_moyenne_unites,
    "temp_min__temp_min" AS temp_min_temp_min,
    "temp_min_units__temp_min_unites" AS temp_min_units_temp_min_unites,
    "temp_max__temp_max" AS temp_max_temp_max,
    "temp_max_units__temp_max_unites" AS temp_max_units_temp_max_unites,
    "total_precip__precip_totale" AS total_precip_precip_totale,
    "total_precip_units__precip_totale_unites" AS total_precip_units_precip_totale_unites,
    "rain__pluie" AS rain_pluie,
    "rain_units__pluie_unites" AS rain_units_pluie_unites,
    "snow__neige" AS snow_neige,
    "snow_units__neige_unites" AS snow_units_neige_unites,
    "pressure_sea_level__pression_niveau_mer" AS pressure_sea_level_pression_niveau_mer,
    "pressure_sea_level_units__pression_niveau_mer_unite" AS pressure_sea_level_units_pression_niveau_mer_unite,
    "pressure_station__pression_station" AS pressure_station_pression_station,
    "pressure_station_units__pression_station_unites" AS pressure_station_units_pression_station_unites,
    "wind_speed__vitesse_vent" AS wind_speed_vitesse_vent,
    "wind_speed_units__vitesse_vent_unites" AS wind_speed_units_vitesse_vent_unites,
    "geometry_type",
    "longitude",
    "latitude"
FROM "environment-and-climate-change-canada-ahccd-annual"
