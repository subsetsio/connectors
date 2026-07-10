-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Event" AS event,
    "Division" AS division,
    "Avg TP, $" AS avg_tp
FROM "fivethirtyeight-nfl-ticket-prices-2014-average-ticket-price"
