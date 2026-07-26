-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_district",
    "category",
    "prek_applicants",
    "prek_offers",
    "kindergarten_applicants",
    "kindergarten_offers",
    "grade_6_applicants",
    "grade_6_offers",
    "grade_9_applicants",
    "grade_9_offers"
FROM "nyc-open-data-evir-bydt"
