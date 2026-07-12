-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "educational_attainment_of_husband_father",
    "family_nucleus_composition_and_children_aged_under_18",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl524.px"
