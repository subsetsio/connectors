-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "demand_type",
    "nw_lhml",
    "magnitude_mw",
    "demand_date_mm_dd_yyyy"
FROM "qatar-planning-and-statistics-authority-sectoral-maximum-electricity-demand-and-dates-mw"
