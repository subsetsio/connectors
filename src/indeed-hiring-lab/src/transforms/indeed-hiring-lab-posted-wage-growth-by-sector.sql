SELECT
    "jobcountry"                                              AS jobcountry,
    "country"                                                 AS country,
    "sector"                                                  AS sector,
    CAST(try_strptime("month", '%b-%y') AS DATE)              AS month,
    TRY_CAST("n_obs" AS BIGINT)                               AS n_obs,
    TRY_CAST("posted_wage_growth_yoy" AS DOUBLE)              AS posted_wage_growth_yoy,
    TRY_CAST("posted_wage_growth_yoy_3moavg" AS DOUBLE)       AS posted_wage_growth_yoy_3moavg
FROM "indeed-hiring-lab-posted-wage-growth-by-sector"
WHERE try_strptime("month", '%b-%y') IS NOT NULL
