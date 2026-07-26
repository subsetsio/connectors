-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "station",
    "street_1",
    "street_2",
    "curb_cut",
    "center_cut",
    "no_curb_cut",
    "ramp_id_no_id_means_a_part_of_center_cut",
    "compliant",
    "slope_112_or_less",
    "slope_noncomp",
    "ramp_width_36_or_more",
    "width_noncomp",
    "lip_or_bump_14_or_less",
    "lip_noncomp",
    "crumbling_concrete",
    "crumbling_noncomp",
    "led_to_pot_hole",
    "pot_hole_noncomp",
    "detectable_warnings",
    "warnings_noncomp",
    "object_barriers",
    "objects_noncomp",
    "barriers_above",
    "ramp_looks_relatively_new"
FROM "nyc-open-data-8kic-uvpz"
