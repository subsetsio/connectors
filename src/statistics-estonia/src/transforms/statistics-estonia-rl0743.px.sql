-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number_of_children_and_age_of_youngest_child",
    "age_of_partner_parent",
    "type_of_family_and_labour_status_of_partners_parents",
    "place_of_residence",
    "indicator",
    "value"
FROM "statistics-estonia-rl0743.px"
