-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_violation_ar",
    "type_of_violation",
    "no_of_violations"
FROM "qatar-planning-and-statistics-authority-traffic-violations-by-type-of-violation"
