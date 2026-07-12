-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include conditional survival across overlapping demographic, stage, and subtype strata; filter to one stratum before comparing survival rates or counts.
SELECT
    "sex",
    "race",
    "age_range",
    "stage",
    "years_since_dx",
    "subtype",
    "site",
    "rate",
    "rate_se",
    "rate_lower_ci",
    "rate_upper_ci",
    "count"
FROM "seer-survival-conditional-survival"
