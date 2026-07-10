-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    "STATE_NAME" AS state_name,
    "COUNTY_NAME" AS county_name,
    CAST("STATE_ID" AS BIGINT) AS state_id,
    CAST("COUNTY_ID" AS BIGINT) AS county_id,
    "PER_CAPITA_EXP_ESRD" AS per_capita_exp_esrd,
    "AVG_RISK_SCORE_ESRD" AS avg_risk_score_esrd,
    "AVG_DEMOG_SCORE_ESRD" AS avg_demog_score_esrd,
    "PERSON_YEARS_ESRD" AS person_years_esrd,
    "PER_CAPITA_EXP_DIS" AS per_capita_exp_dis,
    "AVG_RISK_SCORE_DIS" AS avg_risk_score_dis,
    "AVG_DEMOG_SCORE_DIS" AS avg_demog_score_dis,
    "PERSON_YEARS_DIS" AS person_years_dis,
    "PER_CAPITA_EXP_AGDU" AS per_capita_exp_agdu,
    "AVG_RISK_SCORE_AGDU" AS avg_risk_score_agdu,
    "AVG_DEMOG_SCORE_AGDU" AS avg_demog_score_agdu,
    "PERSON_YEARS_AGDU" AS person_years_agdu,
    "PER_CAPITA_EXP_AGND" AS per_capita_exp_agnd,
    "AVG_RISK_SCORE_AGND" AS avg_risk_score_agnd,
    "AVG_DEMOG_SCORE_AGND" AS avg_demog_score_agnd,
    "PERSON_YEARS_AGND" AS person_years_agnd
FROM "cms-5f9f1216-6fd9-455d-bfbc-0efade687a4e"
