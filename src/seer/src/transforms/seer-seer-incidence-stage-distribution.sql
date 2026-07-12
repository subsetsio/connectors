-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include overlapping demographic strata; filter to one stratum before aggregating stage-distribution percentages or counts.
SELECT
    "sex",
    "race",
    "age_range",
    "stage",
    "site",
    "percent",
    "count"
FROM "seer-seer-incidence-stage-distribution"
