SELECT
    IndicatorCategory            AS indicator_category,
    IndicatorCode                AS indicator_code,
    Indicator                    AS indicator,
    ReporterCode                 AS reporter_code,
    ReporterISO3A                AS reporter_iso3,
    Reporter                     AS reporter,
    PartnerCode                  AS partner_code,
    PartnerISO3A                 AS partner_iso3,
    Partner                      AS partner,
    ProductClassificationCode    AS product_classification_code,
    ProductClassification        AS product_classification,
    ProductCode                  AS product_code,
    Product                      AS product,
    FrequencyCode                AS frequency_code,
    Frequency                    AS frequency,
    UnitCode                     AS unit_code,
    Unit                         AS unit,
    TRY_CAST(Year AS INTEGER)    AS year,
    ValueFlagCode                AS value_flag_code,
    ValueFlag                    AS value_flag,
    TRY_CAST(Value AS DOUBLE)    AS value
FROM "wto-services-annual"
WHERE TRY_CAST(Year AS INTEGER) IS NOT NULL
  AND TRY_CAST(Value AS DOUBLE) IS NOT NULL
