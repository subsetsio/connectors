-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: All three series are TEN-YEAR horizon values in percent per year, and are model estimates (Haubrich-Pennacchi-Ritchken term-structure model), not market observables. The horizon is not encoded in the data.
-- caution: Monthly observations dated to the first of the month; the whole history is re-estimated when the model is refit, so values for past dates can change between runs.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "expected_inflation",
    "real_risk_premium",
    "inflation_risk_premium"
FROM "cleveland-fed-inflationexpectations-inflationexpectations-chart1"
