-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Policy milestone rows are events by state and policy description, not a regular time series; filter the policy_description column before counting policy timing.
SELECT
    "statefips",
    "statename",
    "date",
    "policy_description",
    "schools_first_closed",
    "nonessential_biz_first_closed",
    "stayathome_first_start"
FROM "opportunity-insights-tracker-policy-milestones-state"
