SELECT
    operation,
    admin0_name,
    admin0_pcode,
    admin1_name,
    admin1_pcode,
    admin2_name,
    admin2_pcode,
    TRY_CAST(admin_level AS INTEGER)            AS admin_level,
    TRY_CAST(num_present_idp_ind AS BIGINT)     AS num_present_idp_ind,
    TRY_CAST(substr(reporting_date, 1, 10) AS DATE) AS reporting_date,
    TRY_CAST(year_reporting_date AS INTEGER)    AS year_reporting_date,
    TRY_CAST(month_reporting_date AS INTEGER)   AS month_reporting_date,
    TRY_CAST(round_number AS INTEGER)           AS round_number,
    displacement_reason,
    TRY_CAST(number_males AS BIGINT)            AS number_males,
    TRY_CAST(number_females AS BIGINT)          AS number_females,
    NULLIF(idp_origin_admin1_name, 'Not available')  AS idp_origin_admin1_name,
    NULLIF(idp_origin_admin1_pcode, 'Not available') AS idp_origin_admin1_pcode,
    assessment_type,
    operation_status
FROM "iom-dtm-displacement"
WHERE TRY_CAST(num_present_idp_ind AS BIGINT) IS NOT NULL
