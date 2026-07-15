-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "retrench_total",
    "retrench_resident",
    "retrench_non_resident",
    "incidence_total",
    "incidence_resident",
    "incidence_non_resident"
FROM "sg-data-d-cc9216784a9de451166a236e9f575c45"
