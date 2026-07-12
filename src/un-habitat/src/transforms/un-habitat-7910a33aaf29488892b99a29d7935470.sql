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
    "ancho_via"
FROM "un-habitat-7910a33aaf29488892b99a29d7935470"
