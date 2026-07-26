-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "id",
    "objectid_1",
    "objectid_2",
    "shape_leng",
    "f_all_bids",
    "f_all_bi_1",
    "f_all_bi_2",
    "f_all_bi_3",
    "f_all_bi_4",
    "f_all_bi_6",
    "f_all_bi_7",
    "shape_le_1",
    "shape_ar_1",
    "year_found",
    "shape_area"
FROM "nyc-open-data-7jdm-inj8"
