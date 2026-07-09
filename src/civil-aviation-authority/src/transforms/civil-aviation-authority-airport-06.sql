-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "rundate",
    "this_period",
    "last_period",
    "airport_cluster",
    "rpt_apt_grp_cd",
    "rpt_apt_grp_name",
    "rpt_apt_name",
    "total_atms_tp",
    "atms_pa_tp",
    "atms_cg_tp",
    "total_atms_lp",
    "atms_pa_lp",
    "atms_cg_lp",
    "total_atms_pc",
    "atms_pa_pc",
    "atms_cg_pc",
    "release_period",
    "family",
    "reporting_airport_group_name",
    "reporting_airport_name",
    "total_atms_this_period",
    "atms_passenger_aircraft_this_period",
    "atms_cargo_aircraft_this_period",
    "total_atms_last_period",
    "atms_passenger_aircraft_last_period",
    "atms_cargo_aircraft_last_period",
    "total_atms_percent",
    "atms_passenger_aircraft_percent",
    "atms_cargo_aircraft_percent"
FROM "civil-aviation-authority-airport-06"
