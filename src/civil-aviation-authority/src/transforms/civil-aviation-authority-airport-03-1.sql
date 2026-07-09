-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "rundate",
    "report_period",
    "airport_cluster",
    "rpt_apt_grp_cd",
    "rpt_apt_grp_name",
    "rpt_apt_name",
    "grand_total",
    "air_transport",
    "air_taxi",
    "positioning_flights",
    "local_movements",
    "test_and_training",
    "other_flights",
    "aero_club",
    "private_flights",
    "official",
    "military",
    "business_aviation",
    "release_period",
    "family"
FROM "civil-aviation-authority-airport-03-1"
