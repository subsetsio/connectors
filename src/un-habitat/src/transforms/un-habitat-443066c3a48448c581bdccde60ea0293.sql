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
    "OBJECTID" AS objectid,
    "codciu",
    "ciudad",
    CAST("osm_id" AS BIGINT) AS osm_id,
    "nombre",
    "highway",
    "tipo",
    "longitud_m",
    "descrip",
    "Shape_Leng" AS shape_leng,
    "ancho_via",
    "Shape_Length" AS shape_length,
    "area_m2",
    "Shape_Area" AS shape_area,
    "OBJECTID_2" AS objectid_2,
    "codciu_2",
    "ciudad_2",
    CAST("osm_id_2" AS BIGINT) AS osm_id_2,
    "nombre_2",
    "highway_2",
    "tipo_2",
    "longitud_1",
    "descrip_2",
    "Shape_Le_1" AS shape_le_1,
    "ancho_via_" AS ancho_via_2,
    "OBJECTID_1" AS objectid_1,
    "Id" AS id,
    "categoria",
    "FAM" AS fam
FROM "un-habitat-443066c3a48448c581bdccde60ea0293"
