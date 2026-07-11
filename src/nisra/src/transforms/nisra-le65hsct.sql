-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(A1)" AS tlist_a1,
    "Grouped calendar year" AS grouped_calendar_year,
    "HSCT" AS hsct,
    "Health and Social Care Trust" AS health_and_social_care_trust,
    CAST("Sex" AS BIGINT) AS sex,
    "Sex Label" AS sex_label,
    "UNIT" AS unit,
    CAST("VALUE" AS DOUBLE) AS value
FROM "nisra-le65hsct"
