-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "asset_id",
    "gi_id",
    "dep_contra",
    "dep_cont_1",
    "row_onsite",
    "project_na",
    "asset_type",
    "status",
    "asset_x_co",
    "asset_y_co",
    "borough",
    "sewer_type",
    "outfall",
    "nyc_waters",
    "bbl",
    "secondary_" AS secondary,
    "community_" AS community,
    "city_counc",
    "assembly_d",
    "asset_leng",
    "asset_widt",
    "asset_area",
    "gi_feature",
    "tree_latin",
    "tree_commo",
    "constructi",
    "construc_1",
    "constracte",
    "program_ar",
    "status_gro"
FROM "nyc-open-data-n7f2-dyvt"
