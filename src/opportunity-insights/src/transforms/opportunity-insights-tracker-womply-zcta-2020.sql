-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "zcta",
    "revenue_all_apr2020",
    "revenue_all_jul2020"
FROM "opportunity-insights-tracker-womply-zcta-2020"
