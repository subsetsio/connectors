-- caution: Historical civil penalty actions file is frozen; use the fiscal year and enforcement date columns as source-reported enforcement timing.
SELECT
    CAST("MatterEnforcementFY" AS BIGINT) AS enforcement_fy,
    CAST(TRY_STRPTIME("MatterEnforcementDate", '%m/%d/%Y %H:%M') AS DATE) AS enforcement_date,
    "MatterName" AS matter_name,
    "MatterNumber" AS matter_number,
    "MatterEnforcementType" AS enforcement_type,
    NULLIF(TRIM("Matterhyperlink", '#'), '') AS url,
    "MatterType" AS matter_type
FROM "ftc-ftc-civil-penalty-actions"
