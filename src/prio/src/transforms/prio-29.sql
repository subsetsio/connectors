-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Religious-cleavage rows are dyad-year observations; aggregate by side or year only after choosing the relationship columns needed.
SELECT
    "idv4",
    "idv3",
    "sidea",
    "gwnoa",
    "sideb",
    "year",
    "govrel",
    "rebrel",
    "cleavage",
    "reldiscr",
    "relleg",
    "relfrac",
    "relpol"
FROM "prio-29"
