-- Occupational Employment and Wage Statistics (OES/OEWS) for Colorado areas.
-- Dropped from the raw asset: stateabbrv/statename/stfips (constant Colorado),
-- indcode/indcodetitle/indcodty (constant 'Total All' — this is not an industry
-- breakdown), period/periodtype/pertypdesc (all rows annual), wagesource/wagesrdesc
-- (constant, the OES survey) and udpct/udpctwage/udrnglopct/udrnghipct/udrngmean
-- (constant zero — carry no information in this load).
-- caution: `rate_type` selects the units of every wage column (hourly vs annual).
-- caution: occupation_code mixes SOC major groups (codes ending 0000) with detailed occupations.
-- caution: balance-of-state areas were redefined in 2015; the two definitions coexist.
SELECT
    CAST("areatype" AS BIGINT)   AS area_type,
    "areatyname"                 AS area_type_name,
    CAST("area" AS BIGINT)       AS area_code,
    "areaname"                   AS area_name,
    CAST("periodyear" AS BIGINT) AS period_year,
    "occcode"                    AS occupation_code,
    "codetitle"                  AS occupation_title,
    CAST("occodetype" AS BIGINT) AS occupation_code_system,
    "occodetydesc"               AS occupation_code_system_name,
    CAST("ratetype" AS BIGINT)   AS rate_type,
    "ratetydesc"                 AS rate_type_name,
    CAST("empcount" AS BIGINT)   AS employment,
    CAST("response" AS BIGINT)   AS response_rate,
    CAST("entrywg" AS DOUBLE)    AS entry_wage,
    CAST("experience" AS DOUBLE) AS experienced_wage,
    CAST("mean" AS DOUBLE)       AS mean_wage,
    CAST("pct10" AS DOUBLE)      AS wage_pct10,
    CAST("pct25" AS DOUBLE)      AS wage_pct25,
    CAST("median" AS DOUBLE)     AS median_wage,
    CAST("pct75" AS DOUBLE)      AS wage_pct75,
    CAST("pct90" AS DOUBLE)      AS wage_pct90,
    CAST("wpctrelerr" AS DOUBLE) AS wage_relative_standard_error,
    CAST("epctrelerr" AS DOUBLE) AS employment_relative_standard_error,
    CAST("panelcode" AS BIGINT)  AS panel_code
FROM "colorado-department-of-labor-and-employment-busm-qa5b"
