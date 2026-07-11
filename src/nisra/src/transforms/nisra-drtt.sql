-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(M1)" AS tlist_m1,
    "Month" AS month,
    "HSCT" AS hsct,
    "Health and Social Care Trust" AS health_and_social_care_trust,
    "COT" AS cot,
    "Classification of Test" AS classification_of_test,
    "PRIORITY" AS priority,
    "Priority of Test" AS priority_of_test,
    "TEST" AS test,
    "Type of Test" AS type_of_test,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-drtt"
