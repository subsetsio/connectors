-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is an OECD SDMX cube. Filter to the intended measure, geography, unit, frequency, and other dimensions before aggregating observations.
SELECT
    "ref_area",
    "freq",
    "measure",
    "unit_measure",
    "duration",
    "temp_threshold",
    "ret_period",
    "hurricane_wind_scale",
    "climate_scenario",
    "time_horiz",
    "statistical_operation",
    "anomaly",
    "obs_status",
    "unit_mult",
    "decimals",
    "base_per",
    "robustness",
    "time_period",
    "value"
FROM "oecd-oecd.env.epi:dsd-ech@coas-flood"
