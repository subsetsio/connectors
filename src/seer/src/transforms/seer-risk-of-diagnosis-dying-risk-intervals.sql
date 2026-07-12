-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix diagnosis and death risk types across intervals and demographic strata; filter to one stat type and stratum before comparing risks.
SELECT
    "stat_type",
    "sex",
    "race",
    "age_range",
    "site",
    "risk_interval",
    "risk",
    "risk_lower_ci",
    "risk_upper_ci"
FROM "seer-risk-of-diagnosis-dying-risk-intervals"
