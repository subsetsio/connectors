-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(Q1)" AS tlist_q1,
    "Quarter" AS quarter,
    "HSCT" AS hsct,
    "Health and Social Care Trust" AS health_and_social_care_trust,
    "SPEC" AS spec,
    "Specialty" AS specialty,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-ipwt"
