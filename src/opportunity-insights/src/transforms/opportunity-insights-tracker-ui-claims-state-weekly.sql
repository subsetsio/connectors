-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide unemployment insurance claims table; columns encode program types and initial versus continued claims, so compare like-named measures rather than summing across all claims columns.
SELECT
    "year",
    "month",
    "day_endofweek",
    "statefips",
    "initclaims_count_regular",
    "contclaims_count_regular",
    "initclaims_count_pua",
    "contclaims_count_peuc",
    "contclaims_count_pua",
    "initclaims_count_combined",
    "contclaims_count_combined",
    "initclaims_rate_regular",
    "contclaims_rate_regular",
    "initclaims_rate_pua",
    "contclaims_rate_peuc",
    "contclaims_rate_pua",
    "initclaims_rate_combined",
    "contclaims_rate_combined"
FROM "opportunity-insights-tracker-ui-claims-state-weekly"
