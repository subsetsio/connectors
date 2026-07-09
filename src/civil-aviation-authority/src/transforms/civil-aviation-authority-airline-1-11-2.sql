-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "rundate",
    "report_period",
    "aln_name",
    "acf_name",
    "release_period",
    "family",
    "passenger_acf_km",
    "cargo_acf_km",
    "passenger_stage_flts",
    "cargo_stage_flts",
    "passengers_acf_hours",
    "cargo_acf_hours",
    "passengers_uplifted",
    "seat_km_used_x1000",
    "seat_km_available_x1000",
    "aircraft_in_service_at_year_end",
    "sum_of_hours_used",
    "sum_of_hours_available"
FROM "civil-aviation-authority-airline-1-11-2"
