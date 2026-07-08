SELECT
    CAST(DataId AS BIGINT)                                   AS data_id,
    IndicatorId                                             AS indicator_id,
    Indicator                                              AS indicator,
    DHS_CountryCode                                        AS country_code,
    CountryName                                            AS country_name,
    CAST(SurveyYear AS INTEGER)                            AS survey_year,
    SurveyId                                              AS survey_id,
    NULLIF(CAST(SurveyType AS VARCHAR), '')               AS survey_type,
    CharacteristicCategory                                AS characteristic_category,
    CharacteristicLabel                                   AS characteristic_label,
    NULLIF(CAST(ByVariableLabel AS VARCHAR), '')          AS by_variable_label,
    CAST(Value AS DOUBLE)                                 AS value,
    CAST(IsPreferred AS BOOLEAN)                          AS is_preferred,
    TRY_CAST(NULLIF(CAST(CILow AS VARCHAR), '') AS DOUBLE)    AS ci_low,
    TRY_CAST(NULLIF(CAST(CIHigh AS VARCHAR), '') AS DOUBLE)   AS ci_high,
    TRY_CAST(NULLIF(CAST(Precision AS VARCHAR), '') AS INTEGER) AS precision
FROM "dhs-program-data"
WHERE Value IS NOT NULL
