-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "local_catch_metric_tons",
    "local_catch_per_boats_metric_tons_per_boats",
    "local_catch_per_fishermen_metric_tons_per_fishermen",
    "number_of_boats",
    "number_of_fishermen",
    "aquaculture",
    "average_number_of_fishermen_per_boats_fisherman_per_boat"
FROM "qatar-planning-and-statistics-authority-number-of-boats-and-fishermen-and-the-quantity-of-catch-and-fishing-effort-and-aquaculture"
