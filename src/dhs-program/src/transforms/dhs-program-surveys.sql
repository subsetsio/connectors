SELECT
    SurveyId                                     AS survey_id,
    DHS_CountryCode                              AS country_code,
    CountryName                                  AS country_name,
    CAST(SurveyYear AS INTEGER)                  AS survey_year,
    NULLIF(CAST(SurveyType AS VARCHAR), '')      AS survey_type,
    NULLIF(CAST(RegionName AS VARCHAR), '')      AS region_name,
    NULLIF(CAST(SubregionName AS VARCHAR), '')   AS subregion_name,
    NULLIF(CAST(ImplementingOrg AS VARCHAR), '') AS implementing_org,
    TRY_CAST(NULLIF(CAST(PublicationDate AS VARCHAR), '') AS DATE) AS publication_date,
    TRY_CAST(NULLIF(CAST(ReleaseDate AS VARCHAR), '') AS DATE)     AS release_date,
    TRY_CAST(NULLIF(CAST(FieldworkStart AS VARCHAR), '') AS DATE)  AS fieldwork_start,
    TRY_CAST(NULLIF(CAST(FieldworkEnd AS VARCHAR), '') AS DATE)    AS fieldwork_end,
    TRY_CAST(NULLIF(CAST(NumberOfWomen AS VARCHAR), '') AS BIGINT)      AS number_of_women,
    TRY_CAST(NULLIF(CAST(NumberOfMen AS VARCHAR), '') AS BIGINT)        AS number_of_men,
    TRY_CAST(NULLIF(CAST(NumberofHouseholds AS VARCHAR), '') AS BIGINT) AS number_of_households
FROM "dhs-program-surveys"
WHERE SurveyId IS NOT NULL
