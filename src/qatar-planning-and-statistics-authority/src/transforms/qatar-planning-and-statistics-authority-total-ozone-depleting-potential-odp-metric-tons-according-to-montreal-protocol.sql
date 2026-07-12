-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "total_consumption"
FROM "qatar-planning-and-statistics-authority-total-ozone-depleting-potential-odp-metric-tons-according-to-montreal-protocol"
