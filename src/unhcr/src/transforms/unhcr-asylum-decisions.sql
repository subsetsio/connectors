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
    dec_level AS decision_level,
    dec_pc AS decision_basis,
    CAST(dec_recognized AS BIGINT) AS recognized,
    CAST(dec_other AS BIGINT) AS other_status,
    CAST(dec_rejected AS BIGINT) AS rejected,
    CAST(dec_closed AS BIGINT) AS closed,
    CAST(dec_total AS BIGINT) AS total_decisions
FROM "unhcr-asylum-decisions"
WHERE dec_total IS NOT NULL
