SELECT
    iso_code3,
    country,
    sdg,
    sdg_target,
    indc_text,
    status,
    sector,
    climate_response,
    type_of_information
FROM "wri-ndc-sdg"
WHERE iso_code3 IS NOT NULL
