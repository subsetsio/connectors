-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "feature_id",
    CAST("DATE" AS TIMESTAMP) AS date,
    "IDENTIFIER" AS identifier,
    "STATION_NAME" AS station_name,
    "STATION_NUMBER" AS station_number,
    "PROV_TERR_STATE_LOC" AS prov_terr_state_loc,
    CAST("TIMEZONE_OFFSET" AS DOUBLE) AS timezone_offset,
    "DATA_TYPE_EN" AS data_type_en,
    "DATA_TYPE_FR" AS data_type_fr,
    "PEAK_CODE_EN" AS peak_code_en,
    "PEAK_CODE_FR" AS peak_code_fr,
    "UNITS_EN" AS units_en,
    "UNITS_FR" AS units_fr,
    "SYMBOL_EN" AS symbol_en,
    "SYMBOL_FR" AS symbol_fr,
    "PEAK" AS peak,
    "geometry_type",
    "longitude",
    "latitude"
FROM "environment-and-climate-change-canada-hydrometric-annual-peaks"
