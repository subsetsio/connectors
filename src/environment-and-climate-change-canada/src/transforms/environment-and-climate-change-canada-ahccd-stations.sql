-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "feature_id",
    "identifier__identifiant" AS identifier_identifiant,
    "station_id__id_station" AS station_id_id_station,
    "station_name__nom_station" AS station_name_nom_station,
    "measurement_type__type_mesure" AS measurement_type_type_mesure,
    "period__periode" AS period_periode,
    "trend_value__valeur_tendance" AS trend_value_valeur_tendance,
    "elevation__elevation" AS elevation_elevation,
    "province__province" AS province_province,
    "joined__rejoint" AS joined_rejoint,
    "year_range__annees" AS year_range_annees,
    "start_date__date_debut" AS start_date_date_debut,
    "end_date__date_fin" AS end_date_date_fin,
    "geometry_type",
    "longitude",
    "latitude"
FROM "environment-and-climate-change-canada-ahccd-stations"
