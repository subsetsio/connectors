-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    "status",
    "year",
    "grade",
    "institutions",
    "value"
FROM "geostat-gender-20statistics-education-04-2-number-of-pupils-of-general-education-schools-by-social-status"
