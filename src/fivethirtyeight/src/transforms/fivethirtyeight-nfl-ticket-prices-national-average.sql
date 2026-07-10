-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Genre" AS genre,
    "Avg TP, $" AS avg_tp
FROM "fivethirtyeight-nfl-ticket-prices-national-average"
