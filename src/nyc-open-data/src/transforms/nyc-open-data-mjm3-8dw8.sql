-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_category",
    "geographic_subdivision",
    "school_name",
    "category",
    "cohort_year",
    "cohort",
    "total_cohort",
    "grads",
    "grads_1",
    "total_regents",
    "total_regents_of_cohort",
    "total_regents_of_grads",
    "advanced_regents",
    "advanced_regents_of_cohort",
    "advanced_regents_of_grads",
    "regents_without_advanced",
    "regents_without_advanced_of_cohort",
    "regents_without_advanced_of_grads",
    "_local" AS local,
    "local_of_cohort",
    "local_of_grads",
    "still_enrolled",
    "still_enrolled_1",
    "dropout",
    "dropout_1",
    "sacc_iep_diploma",
    "sacc_iep_diploma_of_cohort",
    "tasc_ged",
    "tasc_ged_of_cohort"
FROM "nyc-open-data-mjm3-8dw8"
