-- NIH RePORTER ExPORTER PROJECT: one row per funded application (APPLICATION_ID).
-- Raw is stringly-typed NDJSON unioned across ~42 fiscal-year batches; every
-- numeric/date column is TRY_CAST (a stray legacy value degrades to NULL rather
-- than failing the node). APPLICATION_ID is the source record key; the QUALIFY
-- guarantees the declared grain even if the source ever repeats an id.
-- SET arrow_large_buffer_size: PROJECT_TERMS / PHR are long free text spanning
-- ~40 years and overflow DuckDB's 2GB regular string buffer when streamed to the
-- Delta writer without 64-bit offsets.
SET arrow_large_buffer_size=true;
SELECT
    TRY_CAST(APPLICATION_ID AS BIGINT)            AS application_id,
    CORE_PROJECT_NUM                              AS core_project_num,
    FULL_PROJECT_NUM                              AS full_project_num,
    SUBPROJECT_ID                                 AS subproject_id,
    TRY_CAST(FY AS INTEGER)                       AS fiscal_year,
    ACTIVITY                                      AS activity_code,
    APPLICATION_TYPE                              AS application_type,
    ADMINISTERING_IC                              AS administering_ic,
    IC_NAME                                       AS ic_name,
    FUNDING_ICS                                   AS funding_ics,
    FUNDING_MECHANISM                             AS funding_mechanism,
    ARRA_FUNDED                                   AS arra_funded,
    -- read_json_auto types this column as JSON over the corpus (it is all-null
    -- in pre-2020s files, so the union widens to JSON); cast to text and strip
    -- the quotes JSON adds around scalar string values.
    trim(CAST(ASSISTANCE_LISTING_NUMBER AS VARCHAR), '"') AS assistance_listing_number,
    OPPORTUNITY_NUMBER                            AS opportunity_number,
    PROJECT_TITLE                                 AS project_title,
    ORG_NAME                                      AS org_name,
    ORG_CITY                                      AS org_city,
    ORG_STATE                                     AS org_state,
    ORG_COUNTRY                                   AS org_country,
    ORG_ZIPCODE                                   AS org_zipcode,
    ORG_DEPT                                      AS org_dept,
    ORG_DUNS                                      AS org_duns,
    ED_INST_TYPE                                  AS ed_inst_type,
    PI_NAMES                                      AS pi_names,
    PI_IDS                                        AS pi_ids,
    PROGRAM_OFFICER_NAME                          AS program_officer_name,
    STUDY_SECTION                                 AS study_section,
    STUDY_SECTION_NAME                            AS study_section_name,
    TRY_CAST(SUPPORT_YEAR AS INTEGER)             AS support_year,
    TRY_CAST(BUDGET_START AS DATE)                AS budget_start,
    TRY_CAST(BUDGET_END AS DATE)                  AS budget_end,
    TRY_CAST(PROJECT_START AS DATE)               AS project_start,
    TRY_CAST(PROJECT_END AS DATE)                 AS project_end,
    TRY_CAST(AWARD_NOTICE_DATE AS DATE)           AS award_notice_date,
    TRY_CAST(DIRECT_COST_AMT AS DOUBLE)           AS direct_cost_amt,
    TRY_CAST(INDIRECT_COST_AMT AS DOUBLE)         AS indirect_cost_amt,
    TRY_CAST(TOTAL_COST AS DOUBLE)                AS total_cost,
    TRY_CAST(TOTAL_COST_SUB_PROJECT AS DOUBLE)    AS total_cost_sub_project,
    PHR                                           AS public_health_relevance
FROM "nih-project"
WHERE TRY_CAST(APPLICATION_ID AS BIGINT) IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY TRY_CAST(APPLICATION_ID AS BIGINT)
    ORDER BY TRY_CAST(FY AS INTEGER) DESC NULLS LAST, FULL_PROJECT_NUM
) = 1
