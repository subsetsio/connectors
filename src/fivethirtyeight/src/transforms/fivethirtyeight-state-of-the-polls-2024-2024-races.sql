-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type",
    "state",
    "seat",
    "num_polls",
    "num_polls_partisan",
    "Cook rating" AS cook_rating
FROM "fivethirtyeight-state-of-the-polls-2024-2024-races"
