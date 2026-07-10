-- caution: Rows are FTC merger enforcement matters; enforcement type and industry are source categories, not mutually exclusive broader market classifications.
SELECT
    CAST("MatterEnforcementFY" AS BIGINT) AS enforcement_fy,
    CAST(TRY_STRPTIME("MatterEnforcementDate", '%m/%d/%Y %H:%M') AS DATE) AS enforcement_date,
    "MatterNumber" AS matter_number,
    "MatterName" AS matter_name,
    "MatterIndustry" AS matter_industry,
    NULLIF(TRIM("Matterhyperlink", '#'), '') AS url,
    "Matter Enforcement Type" AS enforcement_type
FROM "ftc-ftc-merger-enforcement-actions"
