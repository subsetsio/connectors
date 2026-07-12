-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "tree_type",
    "lnw",
    "number_of_trees"
FROM "qatar-planning-and-statistics-authority-number-of-fruit-trees-in-the-registed-farms"
