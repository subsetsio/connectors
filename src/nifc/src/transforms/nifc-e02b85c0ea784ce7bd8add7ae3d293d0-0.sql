-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "IRWINID" AS irwinid,
    "FORID" AS forid,
    "INCIDENT" AS incident,
    "GIS_ACRES" AS gis_acres,
    "UNQE_FIRE_ID" AS unqe_fire_id,
    "DATE_CUR" AS date_cur,
    "FIRE_YEAR_INT" AS fire_year_int,
    "UNIT_ID" AS unit_id,
    "POO_RESP_I" AS poo_resp_i,
    "LOCAL_NUM" AS local_num,
    "FEATURE_CA" AS feature_ca,
    "MAP_METHOD" AS map_method,
    "COMMENTS" AS comments,
    "GEO_ID" AS geo_id,
    "SOURCE" AS source,
    "AGENCY" AS agency,
    CAST("FIRE_YEAR" AS BIGINT) AS fire_year,
    "GlobalID" AS globalid
FROM "nifc-e02b85c0ea784ce7bd8add7ae3d293d0-0"
