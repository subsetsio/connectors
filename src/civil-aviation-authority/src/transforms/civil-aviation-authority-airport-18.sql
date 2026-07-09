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
    "total_ml_pa_tp",
    "total_ml_pa_lp",
    "total_ml_pa_pc",
    "total_ml_cg_tp",
    "total_ml_cg_lp",
    "total_ml_cg_pc",
    "total_ml_tp",
    "total_ml_lp",
    "total_ml_pc",
    "release_period",
    "family",
    "repoting_airport_group_name",
    "reporting_airport_name",
    "total_mail_passenger_aircraft_this_period",
    "total_mail_passenger_aircraft_last_period",
    "total_mail_passenger_aircraft_percent_change",
    "total_mail_cargo_aircraft_this_period",
    "total_mail_cargo_aircraft_last_period",
    "total_mail_cargo_aircraft_percent_change",
    "total_mail_this_period",
    "total_mail_last_period",
    "total_mail_percent_change"
FROM "civil-aviation-authority-airport-18"
