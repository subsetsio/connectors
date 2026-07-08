SELECT
    IndicatorId                                  AS indicator_id,
    Label                                        AS label,
    NULLIF(CAST(Definition AS VARCHAR), '')      AS definition,
    NULLIF(CAST(Level1 AS VARCHAR), '')          AS level1,
    NULLIF(CAST(Level2 AS VARCHAR), '')          AS level2,
    NULLIF(CAST(Level3 AS VARCHAR), '')          AS level3,
    NULLIF(CAST(MeasurementType AS VARCHAR), '') AS measurement_type,
    NULLIF(CAST(IndicatorType AS VARCHAR), '')   AS indicator_type,
    NULLIF(CAST(Denominator AS VARCHAR), '')     AS denominator,
    NULLIF(CAST(ShortName AS VARCHAR), '')       AS short_name,
    NULLIF(CAST(TagIds AS VARCHAR), '')          AS tag_ids,
    CAST(IsQuickStat AS BOOLEAN)                 AS is_quick_stat
FROM "dhs-program-indicators"
WHERE IndicatorId IS NOT NULL
