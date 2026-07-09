-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "gainer",
    "gaintype",
    "procedur",
    "entity",
    "contgain",
    "area",
    "pop",
    "portion",
    "loser",
    "losetype",
    "contlose",
    "entry",
    "exit",
    "number",
    "indep",
    "conflict",
    "version"
FROM "correlates-of-war-territorial-change"
