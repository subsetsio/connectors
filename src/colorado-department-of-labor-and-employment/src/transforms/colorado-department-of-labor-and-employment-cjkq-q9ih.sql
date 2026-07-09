-- Quarterly Census of Employment and Wages (QCEW): employer, employment and wage
-- counts by industry and ownership for Colorado areas.
-- Dropped from the raw asset: stateabbrv, statename, stfips (constant Colorado),
-- indcodty (constant NAICS coding system) and suppress (constant 0 — nothing is
-- suppressed in the current load).
-- caution: annual and quarterly rows coexist (period_type); filter before summing wages.
-- caution: industry_code and ownership_code both contain aggregate rows above their components.
SELECT
    CAST("areatype" AS BIGINT)   AS area_type,
    "areatyname"                 AS area_type_name,
    CAST("area" AS BIGINT)       AS area_code,
    "areaname"                   AS area_name,
    CAST("periodyear" AS BIGINT) AS period_year,
    CAST("periodtype" AS BIGINT) AS period_type,
    "pertypdesc"                 AS period_type_name,
    CAST("period" AS BIGINT)     AS period,
    "indcode"                    AS industry_code,
    "codetitle"                  AS industry_title,
    "ownership"                  AS ownership_code,
    "ownertitle"                 AS ownership_title,
    CAST("prelim" AS BOOLEAN)    AS preliminary,
    CAST("firms" AS BIGINT)      AS firms,
    CAST("estab" AS BIGINT)      AS establishments,
    CAST("avgemp" AS BIGINT)     AS average_employment,
    CAST("mnth1emp" AS BIGINT)   AS month1_employment,
    CAST("mnth2emp" AS BIGINT)   AS month2_employment,
    CAST("mnth3emp" AS BIGINT)   AS month3_employment,
    CAST("topempav" AS BIGINT)   AS top_employer_average_employment,
    CAST("totwage" AS BIGINT)    AS total_wages,
    CAST("avgwkwage" AS BIGINT)  AS average_weekly_wage,
    CAST("taxwage" AS BIGINT)    AS taxable_wages,
    CAST("contrib" AS BIGINT)    AS contributions
FROM "colorado-department-of-labor-and-employment-cjkq-q9ih"
