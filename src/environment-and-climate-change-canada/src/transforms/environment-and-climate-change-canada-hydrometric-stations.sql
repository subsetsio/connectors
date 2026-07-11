-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "feature_id",
    "STATION_NAME" AS station_name,
    "IDENTIFIER" AS identifier,
    "STATION_NUMBER" AS station_number,
    "PROV_TERR_STATE_LOC" AS prov_terr_state_loc,
    "STATUS_EN" AS status_en,
    "STATUS_FR" AS status_fr,
    "CONTRIBUTOR_EN" AS contributor_en,
    "CONTRIBUTOR_FR" AS contributor_fr,
    "VERTICAL_DATUM" AS vertical_datum,
    "REAL_TIME" AS real_time,
    "RHBN" AS rhbn,
    "DRAINAGE_AREA_GROSS" AS drainage_area_gross,
    "DRAINAGE_AREA_EFFECT" AS drainage_area_effect,
    "geometry_type",
    "longitude",
    "latitude"
FROM "environment-and-climate-change-canada-hydrometric-stations"
