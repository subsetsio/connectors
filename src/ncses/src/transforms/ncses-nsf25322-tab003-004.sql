-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide NCSES source table with no scan-verified row identifier; treat rows as source cross-tab records and use the table title and column labels to determine aggregation scope before summing.
SELECT
    "Sex occupation and job satisfaction" AS sex_occupation_and_job_satisfaction,
    "Total" AS total,
    "Years since highest degreea - < 5" AS years_since_highest_degreea_5,
    "Years since highest degreea - 5–9" AS years_since_highest_degreea_5_9,
    "Years since highest degreea - 10–14" AS years_since_highest_degreea_10_14,
    "Years since highest degreea - 15–19" AS years_since_highest_degreea_15_19,
    "Years since highest degreea - 20–24" AS years_since_highest_degreea_20_24,
    "Years since highest degreea - 25–29" AS years_since_highest_degreea_25_29,
    "Years since highest degreea - 30–34" AS years_since_highest_degreea_30_34,
    "Years since highest degreea - ≥ 35" AS years_since_highest_degreea_35
FROM "ncses-nsf25322-tab003-004"
