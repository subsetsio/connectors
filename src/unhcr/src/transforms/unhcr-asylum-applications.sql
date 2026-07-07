SELECT
    CAST("year" AS BIGINT) AS year,
    CAST(coo_id AS BIGINT) AS origin_id,
    coo AS origin_code,
    coo_iso AS origin_iso3,
    trim(coo_name) AS origin_name,
    CAST(coa_id AS BIGINT) AS asylum_country_id,
    coa AS asylum_country_code,
    coa_iso AS asylum_country_iso3,
    trim(coa_name) AS asylum_country_name,
    procedure_type,
    app_type AS application_type,
    dec_level AS decision_level,
    app_pc AS application_basis,
    CAST(applied AS BIGINT) AS applications
FROM "unhcr-asylum-applications"
WHERE applied IS NOT NULL
