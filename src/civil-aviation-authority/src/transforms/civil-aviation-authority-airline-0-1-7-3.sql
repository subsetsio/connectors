-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "rundate",
    "report_period",
    "major_break",
    "aln_name",
    "acf_km",
    "no_flights",
    "acf_hours",
    "tot_rev_p_ca",
    "seat_km_avl",
    "seat_km_used",
    "tot_rev_wt",
    "tot_tn_km_avl",
    "tot_ml_tn_km",
    "tot_fr_tn_km",
    "tot_p_tn_km",
    "release_period",
    "family",
    "reporting_period",
    "type_of_operation",
    "airline_name",
    "aircraft_km_x1000",
    "aircraft_hours",
    "total_passengers_uplifted",
    "seat_km_available_x1000",
    "seat_km_used_x1000",
    "cargo_tonnes_uplifted",
    "total_tonne_km_available_x1000",
    "total_mail_tonne_km_used_x1000",
    "total_freight_tonne_km_used_x1000",
    "total_passenger_tonne_km_used_x1000"
FROM "civil-aviation-authority-airline-0-1-7-3"
