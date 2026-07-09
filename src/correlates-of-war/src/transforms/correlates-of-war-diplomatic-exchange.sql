-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ccode1",
    "ccode2",
    "year",
    "DR_at_1" AS dr_at_1,
    "DR_at_2" AS dr_at_2,
    "DE" AS de,
    "version"
FROM "correlates-of-war-diplomatic-exchange"
