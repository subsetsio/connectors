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
    "total_fr_pa_tp",
    "total_fr_pa_lp",
    "total_fr_pa_pc",
    "total_fr_cg_tp",
    "total_fr_cg_lp",
    "total_fr_cg_pc",
    "total_fr_tp",
    "total_fr_lp",
    "total_fr_pc",
    "release_period",
    "family",
    "reporting_airport_group_name",
    "reporting_airport_name",
    "total_freight_passenger_aircraft_this_period",
    "total_freight_passenger_aircraft_last_period",
    "total_freight_passenger_aircraft_percent_change",
    "total_freight_cargo_aircraft_this_period",
    "total_freight_cargo_aircraft_last_period",
    "total_freight_cargo_aircraft_percent_change",
    "total_freight_this_period",
    "total_freight_last_period",
    "total_freight_percent_change"
FROM "civil-aviation-authority-airport-15"
