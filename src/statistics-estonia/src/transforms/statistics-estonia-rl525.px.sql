-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are not uniquely keyed by the exposed PxWeb label dimensions in the raw download; duplicate label-level combinations exist, so no table-level grain is asserted.
SELECT
    "age_of_the_spouse_parent",
    "family_nucleus_composition_and_economic_activity_of_members",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rl525.px"
