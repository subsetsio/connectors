-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "street_1",
    "street_2",
    "curb_cut",
    "slope_inch",
    "ramp_width",
    "no_curb_cut",
    "center_cut",
    "lipbump_measurement_in_inches",
    "crumbling_concrete",
    "led_to_pot_hole",
    "detectable_warnings",
    "object_barriers",
    "barriers_above"
FROM "nyc-open-data-4y9q-t4wb"
