-- caution: Rows are FTC nonmerger enforcement matters; the upstream CSV contains at least one exact duplicate row, and industry is a source category rather than a complete industry taxonomy.
SELECT DISTINCT
    CAST("MatterEnforcementFY" AS BIGINT) AS enforcement_fy,
    CAST(TRY_STRPTIME("MatterEnforcementDate", '%m/%d/%Y %H:%M') AS DATE) AS enforcement_date,
    "MatterNumber" AS matter_number,
    "MatterName" AS matter_name,
    "MatterEnforcementType" AS enforcement_type,
    "MatterIndustry" AS matter_industry,
    NULLIF(TRIM("Matterhyperlink", '#'), '') AS url
FROM "ftc-ftc-nonmerger-enforcement-actions"
