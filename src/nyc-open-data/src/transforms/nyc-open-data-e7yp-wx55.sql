-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "pay_by_cel",
    "vehicle_ty",
    "all_vehicl",
    "all_vehi_1",
    "all_vehi_2",
    "all_vehi_3",
    "commercial",
    "commerci_1",
    "commerci_2",
    "commerci_3",
    "on_street",
    "side_of_st",
    "from_stree",
    "to_street",
    "borough",
    "meter_rate",
    "shape_leng"
FROM "nyc-open-data-e7yp-wx55"
