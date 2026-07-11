-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(A1)" AS tlist_a1,
    "Academic year" AS academic_year,
    "HSCT" AS hsct,
    "Health and Social Care Trust" AS health_and_social_care_trust,
    "ATTAIN" AS attain,
    "Attainment" AS attainment,
    "FSME" AS fsme,
    "Free school meal entitlement" AS free_school_meal_entitlement,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-deslsahsct"
