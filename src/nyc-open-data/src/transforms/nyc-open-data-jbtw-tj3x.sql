-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_month" AS month,
    "bus_company",
    "count_of_students_traveling_to_school_assigned_to_stopto_school_to_school_routes",
    "count_of_students_traveling_from_school_assigned_to_stoptoschool_to_school_routes"
FROM "nyc-open-data-jbtw-tj3x"
