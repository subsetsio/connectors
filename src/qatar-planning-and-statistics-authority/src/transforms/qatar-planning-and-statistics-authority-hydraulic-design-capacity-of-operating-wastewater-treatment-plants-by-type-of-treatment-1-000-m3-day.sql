-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "indicator_name",
    "value_thousand_cubic_metre_day"
FROM "qatar-planning-and-statistics-authority-hydraulic-design-capacity-of-operating-wastewater-treatment-plants-by-type-of-treatment-1-000-m3-day"
