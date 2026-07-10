-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Income columns are monthly real values expressed in 2005 USD PPP; compare or aggregate them as income distribution measures, not annual totals.
SELECT
    "country",
    "year",
    "decile_1_income",
    "decile_2_income",
    "decile_3_income",
    "decile_4_income",
    "decile_5_income",
    "decile_6_income",
    "decile_7_income",
    "decile_8_income",
    "decile_9_income",
    "decile_10_income",
    "mean_income",
    "population"
FROM "gcip-gcip-income-deciles"
