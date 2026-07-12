-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a geodatabase-derived CPI feature table; rows are spatial features, not pre-aggregated city totals.
SELECT
    "source_item_id",
    "source_title",
    "source_type",
    "source_kind",
    "source_name",
    "source_row_number",
    "OBJECTID_1" AS objectid_1,
    "OBJECTID" AS objectid,
    "codciu",
    "ciudad",
    "area_m2",
    "Shape_Leng" AS shape_leng,
    "Shape_Le_1" AS shape_le_1,
    "Shape_Length" AS shape_length,
    "Shape_Area" AS shape_area,
    "nombre",
    "tipo",
    "FAM" AS fam,
    "descrip",
    "categoria",
    "Id" AS id,
    CAST("osm_id" AS BIGINT) AS osm_id,
    "highway",
    "longitud_m",
    "ancho_via",
    "OBJECTID_2" AS objectid_2,
    "codciu_2",
    "ciudad_2",
    CAST("osm_id_2" AS BIGINT) AS osm_id_2,
    "nombre_2",
    "highway_2",
    "tipo_2",
    "longitud_1",
    "descrip_2",
    "ancho_via_" AS ancho_via_2
FROM "un-habitat-52a16862bcc942f29c877dea2615a765"
