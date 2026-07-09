-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dyad",
    "statelno",
    "statelab",
    "statehno",
    "statehab",
    "conttype",
    "begin",
    "end",
    "notes",
    "version"
FROM "correlates-of-war-direct-contiguity"
