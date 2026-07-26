-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "feeder_school_dbn",
    "feeder_school_name",
    "count_of_students_in_hs_admissions",
    "count_of_testers",
    "number_of_offers",
    "number_of_discovery_participants"
FROM "nyc-open-data-k8ah-28f4"
