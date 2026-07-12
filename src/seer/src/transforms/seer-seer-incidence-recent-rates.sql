-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include overlapping demographic, stage, and subtype strata; filter to one stratum before aggregating recent incidence rates or counts.
SELECT
    "sex",
    "race",
    "age_range",
    "stage",
    "subtype",
    "site",
    "rate",
    "rate_se",
    "rate_lower_ci",
    "rate_upper_ci",
    "count"
FROM "seer-seer-incidence-recent-rates"
