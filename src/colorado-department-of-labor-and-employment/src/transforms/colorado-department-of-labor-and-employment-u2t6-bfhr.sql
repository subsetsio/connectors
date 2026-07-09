-- Short-term (two-year) employment projections for Colorado, by industry and occupation.
-- Dropped from the raw asset: stateabbrv, statename, stfips (constant Colorado),
-- matincodty/matoccodty (constant coding-system codes), periodtype (constant) and
-- suppress (constant 0 — nothing is withheld in this load).
-- caution: not a time series — base_employment and projected_employment are two
--          points in time on the SAME row, named by projection_period.
-- caution: industry_code and occupation_code are hierarchies containing total rows.
SELECT
    CAST("areatype" AS BIGINT)   AS area_type,
    "areatyname"                 AS area_type_name,
    CAST("area" AS BIGINT)       AS area_code,
    "areaname"                   AS area_name,
    CAST("periodid" AS BIGINT)   AS projection_id,
    "perioddesc"                 AS projection_period,
    CAST("matincode" AS BIGINT)  AS industry_code,
    "matintitle"                 AS industry_title,
    CAST("matoccode" AS BIGINT)  AS occupation_code,
    "matocctitl"                 AS occupation_title,
    CAST("estemp" AS BIGINT)     AS base_employment,
    CAST("projemp" AS BIGINT)    AS projected_employment,
    CAST("nchg" AS BIGINT)       AS employment_change,
    CAST("pchg" AS DOUBLE)       AS percent_change,
    CAST("growrate" AS DOUBLE)   AS annual_growth_rate,
    CAST("pctestind" AS DOUBLE)  AS base_share_of_industry,
    CAST("pctprojind" AS DOUBLE) AS projected_share_of_industry,
    CAST("pctestocc" AS DOUBLE)  AS base_share_of_occupation,
    CAST("pctprojocc" AS DOUBLE) AS projected_share_of_occupation
FROM "colorado-department-of-labor-and-employment-u2t6-bfhr"
