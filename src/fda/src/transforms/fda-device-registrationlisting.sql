-- fda-device-registrationlisting: Establishment registration x device listing; the source flattens one row per registration-listing-premarket link, with no natural unique key — published keyless.
SELECT
    NULLIF(trim("registration_number"), '') AS registration_number,
    NULLIF(trim("fei_number"), '') AS fei_number,
    "name" AS name,
    TRY_CAST(TRY_CAST("status_code" AS DOUBLE) AS INTEGER) AS status_code,
    "initial_importer_flag" AS initial_importer_flag,
    TRY_CAST(TRY_CAST("reg_expiry_date_year" AS DOUBLE) AS INTEGER) AS reg_expiry_date_year,
    "address_line_1" AS address_line_1,
    NULLIF(trim("city"), '') AS city,
    NULLIF(trim("state_code"), '') AS state_code,
    NULLIF(trim("iso_country_code"), '') AS iso_country_code,
    NULLIF(trim("zip_code"), '') AS zip_code,
    "owner_operator_firm_name" AS owner_operator_firm_name,
    NULLIF(trim("k_number"), '') AS k_number,
    NULLIF(trim("pma_number"), '') AS pma_number,
    "establishment_type" AS establishment_type,
    NULLIF(trim("proprietary_name"), '') AS proprietary_name
FROM "fda-device-registrationlisting"
