-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ccode",
    "statename",
    "stateabb",
    "year",
    "imports",
    "exports",
    "alt_imports",
    "alt_exports",
    "source1",
    "source2",
    "version"
FROM "correlates-of-war-trade-national"
