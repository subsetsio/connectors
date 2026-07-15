-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "date_figure",
    "confirmed_total",
    "daily_cases",
    "discharge_volume",
    "discharge_total",
    "hospitalised_total",
    "hopitalised_critical",
    "hospitalised_stable"
FROM "sg-data-d-37c77bafba57a15da0da74326d6cc077"
