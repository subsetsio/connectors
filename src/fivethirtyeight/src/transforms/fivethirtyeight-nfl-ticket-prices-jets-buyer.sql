-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Raiders at Jets 9/7/14" AS raiders_at_jets_9_7_14,
    "C1" AS c1,
    "_1" AS "1"
FROM "fivethirtyeight-nfl-ticket-prices-jets-buyer"
