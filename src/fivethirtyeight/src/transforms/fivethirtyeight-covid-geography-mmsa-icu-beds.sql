-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MMSA" AS mmsa,
    "total_percent_at_risk",
    "high_risk_per_ICU_bed" AS high_risk_per_icu_bed,
    "high_risk_per_hospital",
    "icu_beds",
    "hospitals",
    "total_at_risk"
FROM "fivethirtyeight-covid-geography-mmsa-icu-beds"
