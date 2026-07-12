-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "families_and_number_of_children_aged_under_18",
    "indicator",
    "type_of_family_and_labour_status_of_partners_parents",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl0741.px"
