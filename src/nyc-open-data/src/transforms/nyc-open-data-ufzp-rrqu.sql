-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "cornerid",
    "rampid",
    "ramp_onstreet",
    "geocyclora",
    "borough",
    "stname1",
    "stname2",
    "curb_reveal",
    "ramp_running_slope_total",
    "dws_conditions",
    "gutter_slope",
    "lnd_width",
    "lnd_length",
    "lnd_cross_slope",
    "counter_slope",
    "ramp_width",
    "ramp_right_flare",
    "ramp_left_flare",
    "ramp_length",
    "ramp_cross_slope",
    "ponding",
    "obstacles_ramp",
    "obstacles_landing"
FROM "nyc-open-data-ufzp-rrqu"
