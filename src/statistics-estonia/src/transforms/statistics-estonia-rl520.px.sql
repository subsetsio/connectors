-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are not uniquely keyed by the exposed PxWeb label dimensions in the raw download; duplicate label-level combinations exist, so no table-level grain is asserted.
SELECT
    "households_with_and_without_unemployed_members",
    "number_of_children_aged_under_18_and_dependants",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl520.px"
