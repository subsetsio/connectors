SELECT
    data_element_name,
    preferred_physical_name,
    description_text,
    unit_of_measure,
    value_domain,
    business_owner_name,
    data_asset_abbreviation,
    data_asset_name,
    subject_category_code,
    data_type_code,
    TRY_CAST(maximum_length AS INTEGER) AS maximum_length,
    TRY_CAST(precision_number AS INTEGER) AS precision_number,
    pattern_text,
    system_number
FROM "fhwa-nhvr-exvq"
WHERE preferred_physical_name IS NOT NULL
