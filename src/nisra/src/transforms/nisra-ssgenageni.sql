-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    "TLIST(A1)" AS tlist_a1,
    "Financial year" AS financial_year,
    "Gender" AS gender,
    "Gender Label" AS gender_label,
    "Age" AS age,
    "Age Label" AS age_label,
    "Arrest" AS arrest,
    "Person subsequently arrested" AS person_subsequently_arrested,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "nisra-ssgenageni"
