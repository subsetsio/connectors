-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "street",
    "trafdir",
    "segmentid",
    "rw_type",
    "streetwidt",
    "boro",
    "facility",
    "direction",
    "_hours" AS hours,
    "_days" AS days,
    "days_code",
    "lane_width",
    "lane_type1",
    "lane_type",
    "lane_descr",
    "lane_color",
    "sbs_route1",
    "sbs_route2",
    "sbs_route3",
    "open_dates",
    "year1",
    "year2",
    "year3",
    "last_updat",
    "chron_id_1",
    "shape_leng",
    "shape_le_1",
    "mid_block"
FROM "nyc-open-data-ycrg-ses3"
