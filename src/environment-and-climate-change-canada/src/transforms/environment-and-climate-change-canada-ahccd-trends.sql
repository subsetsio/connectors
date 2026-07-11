-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "feature_id",
    "identifier__identifiant" AS identifier_identifiant,
    "station_id__id_station" AS station_id_id_station,
    "station_name__nom_station" AS station_name_nom_station,
    "joined__rejoint" AS joined_rejoint,
    "elevation__elevation" AS elevation_elevation,
    "period__periode" AS period_periode,
    "province__province" AS province_province,
    "year_range__annees" AS year_range_annees,
    "measurement_type__type_mesure" AS measurement_type_type_mesure,
    "trend_value__valeur_tendance" AS trend_value_valeur_tendance,
    "geometry_type",
    "longitude",
    "latitude"
FROM "environment-and-climate-change-canada-ahccd-trends"
