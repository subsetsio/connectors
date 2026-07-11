-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "feature_id",
    "IDENTIFIER" AS identifier,
    "STATION_NAME" AS station_name,
    "STATION_NUMBER" AS station_number,
    "PROV_TERR_STATE_LOC" AS prov_terr_state_loc,
    "DATA_TYPE_EN" AS data_type_en,
    "DATA_TYPE_FR" AS data_type_fr,
    "MAX_DATE" AS max_date,
    "MAX_SYMBOL_EN" AS max_symbol_en,
    "MAX_SYMBOL_FR" AS max_symbol_fr,
    "MAX_VALUE" AS max_value,
    "MIN_DATE" AS min_date,
    "MIN_SYMBOL_EN" AS min_symbol_en,
    "MIN_SYMBOL_FR" AS min_symbol_fr,
    "MIN_VALUE" AS min_value,
    "geometry_type",
    "longitude",
    "latitude"
FROM "environment-and-climate-change-canada-hydrometric-annual-statistics"
