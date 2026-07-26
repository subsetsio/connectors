-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough",
    "censusblock_2000",
    "censusblock_2000_suffix",
    "censustract_2000",
    "censusblock_2010",
    "censusblock_2010_suffix",
    "censustract_2010",
    "censustract_1990",
    "admin_fire",
    "water_flag",
    "assemdist",
    "electdist",
    "schooldist",
    "commdist",
    "sb1_volume",
    "sb1_page",
    "sb2_volume",
    "sb2_page",
    "sb3_volume",
    "sb3_page",
    "atomicid",
    "atomic_num",
    "hurricane_evacuation_zone",
    "censustract_2020",
    "censusblock_2020",
    "censusblock_2020_suffix",
    "commercial_waste_zone",
    "shape_area",
    "shape_length",
    "the_geom"
FROM "nyc-open-data-wgbs-damt"
