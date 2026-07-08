SELECT DISTINCT
    reference_period,
    nca_iso_code,
    reporting_country,
    undertaking_type,
    cic_main_category,
    cic_sub_category,
    portfolio_type,
    location_of_investment,
    real_estate_exposure,
    type_of_real_estate_exposure,
    CAST(value_eur_millions AS DOUBLE) AS value_eur_millions,
    CAST(try_strptime(extraction_date, '%Y%m%d') AS DATE) AS extraction_date
FROM "eiopa-solo-asset-exposures"
WHERE value_eur_millions IS NOT NULL
