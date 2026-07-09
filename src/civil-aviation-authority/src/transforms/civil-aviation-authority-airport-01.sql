-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "rundate",
    "report_period",
    "airport_name",
    "this_year_pax",
    "this_year_total_pax",
    "Five_years_prev_pax" AS five_years_prev_pax,
    "Five_years_prev_pax_total" AS five_years_prev_pax_total,
    "release_period",
    "family"
FROM "civil-aviation-authority-airport-01"
