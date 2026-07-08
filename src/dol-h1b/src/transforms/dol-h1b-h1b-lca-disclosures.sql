SELECT
    CAST(fiscal_year AS INTEGER)        AS fiscal_year,
    NULLIF(quarter, '')                 AS quarter,
    UPPER(NULLIF(case_status, ''))      AS case_status,
    NULLIF(employer_name, '')           AS employer_name,
    NULLIF(employer_state, '')          AS employer_state,
    NULLIF(employer_city, '')           AS employer_city,
    NULLIF(job_title, '')               AS job_title,
    NULLIF(soc_code, '')                AS soc_code,
    NULLIF(soc_title, '')               AS soc_title,
    NULLIF(wage_rate, '')               AS wage_rate,
    UPPER(NULLIF(wage_unit, ''))        AS wage_unit,
    NULLIF(worksite_state, '')          AS worksite_state,
    NULLIF(worksite_city, '')           AS worksite_city,
    -- Extract the leading numeric token: handles plain values
    -- ("143666"), decimals ("42.53"), and the FY2015 range format
    -- ("18.49 -") which a bare CAST cannot parse.
    TRY_CAST(
        regexp_extract(
            REPLACE(REPLACE(NULLIF(wage_rate, ''), ',', ''), '$', ''),
            '[0-9]+\.?[0-9]*', 0
        ) AS DOUBLE
    ) AS wage_rate_numeric
FROM "dol-h1b-h1b-lca-disclosures"
WHERE fiscal_year IS NOT NULL
  AND (employer_name IS NOT NULL OR case_status IS NOT NULL)
