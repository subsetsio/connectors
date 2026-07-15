-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry",
    "no_of_tu"
FROM "sg-data-d-d2448eb62adf0337ca58c037c6cc3633"
