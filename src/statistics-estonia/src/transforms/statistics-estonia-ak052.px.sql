-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "residence_of_household",
    "primary_activity",
    "sex",
    "period",
    "value"
FROM "statistics-estonia-ak052.px"
