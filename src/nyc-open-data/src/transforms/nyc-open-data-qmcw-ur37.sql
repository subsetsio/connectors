-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "objectid",
    "borocode",
    "boroct",
    "bldgarea",
    "resarea",
    "res_pct",
    "totalpop",
    "lowmod_population",
    "lomod_pct",
    "eligibility",
    "ct_text"
FROM "nyc-open-data-qmcw-ur37"
