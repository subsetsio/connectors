-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "STATISTIC Label" AS statistic_label,
    "TLIST(A1)" AS tlist_a1,
    "Financial Year" AS financial_year,
    "HSCT" AS hsct,
    "Health and Social Care Trust" AS health_and_social_care_trust,
    "UNIT" AS unit,
    CAST("VALUE" AS DOUBLE) AS value
FROM "nisra-othscrt1"
