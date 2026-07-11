-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "jobcountry",
    "country",
    "sector",
    "month",
    CAST("n_obs" AS BIGINT) AS n_obs,
    CAST("posted_wage_growth_yoy" AS DOUBLE) AS posted_wage_growth_yoy,
    "posted_wage_growth_yoy_3moavg",
    "month_date"
FROM "indeed-hiring-lab-posted-wage-growth-by-sector"
