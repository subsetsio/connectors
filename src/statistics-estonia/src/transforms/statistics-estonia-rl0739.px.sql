-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "educational_attainment_of_woman",
    "indicator",
    "families_and_number_of_children_aged_under_18",
    "type_of_family",
    "county",
    "value"
FROM "statistics-estonia-rl0739.px"
