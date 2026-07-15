-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "ind1",
    "ind2",
    "bwc"
FROM "sg-data-d-bd83b4534db1032ca7415f82bbaae003"
