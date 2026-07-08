SELECT
    country,
    NULLIF(region, '0')    AS region,
    NULLIF(residence, '0') AS residence,
    NULLIF(ethnicity, '0') AS ethnicity,
    NULLIF(socdem, '0')    AS socdem,
    CAST(version AS INTEGER) AS version,
    ref_id,
    CAST(year1 AS INTEGER) AS year_start,
    CAST(year2 AS INTEGER) AS year_end,
    CAST(type_lt AS INTEGER) AS life_table_type,
    CAST(sex AS INTEGER)     AS sex,
    CAST(age AS INTEGER)     AS age,
    CAST(age_int AS INTEGER) AS age_interval,
    CAST(mx AS DOUBLE)  AS death_rate_mx,
    CAST(qx AS DOUBLE)  AS death_probability_qx,
    CAST(lx AS DOUBLE)  AS survivors_lx,
    CAST(dx AS DOUBLE)  AS deaths_dx,
    CAST("Lx" AS DOUBLE) AS person_years_Lx,
    CAST("Tx" AS DOUBLE) AS total_years_Tx,
    CAST(ex AS DOUBLE)      AS life_expectancy_ex,
    CAST(ex_orig AS DOUBLE) AS life_expectancy_orig_ex
FROM "hld-life-tables"
WHERE country IS NOT NULL
