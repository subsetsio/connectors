-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "abc",
    "name",
    "year",
    "gwno_a",
    "newconf",
    "onset1",
    "onset2",
    "onset3",
    "onset5",
    "onset10",
    "onset20",
    "              conflict_ids" AS conflict_ids,
    "year_prev"
FROM "ucdp-onset-intrastate-country"
