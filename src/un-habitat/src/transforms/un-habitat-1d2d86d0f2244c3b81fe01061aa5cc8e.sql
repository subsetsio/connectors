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
    "osm_id",
    "name",
    "highway",
    "Tipo_1" AS tipo_1,
    "longitud_m",
    "ancho_via",
    "OBJECTID_2" AS objectid_2,
    "osm_id_2",
    "name_2",
    "highway_2",
    "Tipo_2" AS tipo_2,
    "codciu_2",
    "ciudad_2",
    "longitud_1",
    "descrip_2",
    "ancho_via_" AS ancho_via_2
FROM "un-habitat-1d2d86d0f2244c3b81fe01061aa5cc8e"
