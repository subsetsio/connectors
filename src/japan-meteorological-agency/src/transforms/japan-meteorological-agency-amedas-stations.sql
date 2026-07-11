-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("station_id" AS BIGINT) AS station_id,
    "type",
    "elems",
    "lat",
    "lon",
    "alt",
    "name_ja",
    "name_kana",
    "name_en"
FROM "japan-meteorological-agency-amedas-stations"
