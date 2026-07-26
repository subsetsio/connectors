-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "evnt_key",
    "violation_date",
    "violation_time",
    "chg_law_cd",
    "violation_code",
    "veh_category",
    "reg_plate_num",
    "reg_state_cd",
    "city_nm",
    "rpt_owning_cmd",
    "x_coord_cd",
    "y_coord_cd",
    "latitude",
    "longitude",
    "location_point",
    "juris_cd"
FROM "nyc-open-data-57p3-pdcj"
