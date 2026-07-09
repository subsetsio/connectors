-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "value",
    "data_marking",
    "years_quarters_months",
    "time",
    "administrative_geography",
    "geography",
    "seasonal_adjustment",
    "seasonaladjustment",
    "construction_series_type",
    "seriestype",
    "construction_classifications",
    "typeofwork"
FROM "ons-output-in-the-construction-industry"
