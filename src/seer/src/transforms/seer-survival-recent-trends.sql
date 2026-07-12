-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include relative-survival intervals across overlapping demographic and stage strata; filter to one stratum before aggregating year-level survival rates or counts.
SELECT
    "relative_survival_interval",
    "sex",
    "race",
    "age_range",
    "stage",
    "site",
    "year",
    "rel_rate",
    "rel_rate_se",
    "rel_rate_lower_ci",
    "rel_rate_upper_ci",
    "modeled_rel_rate",
    "count"
FROM "seer-survival-recent-trends"
