SELECT
    TRY_CAST(MatterEnforcementFY AS INTEGER)              AS enforcement_fy,
    TRY_STRPTIME(MatterEnforcementDate, '%m/%d/%Y %H:%M')::DATE AS enforcement_date,
    MatterNumber                                         AS matter_number,
    MatterName                                           AS matter_name,
    MatterEnforcementType                                AS enforcement_type,
    MatterIndustry                                       AS matter_industry,
    NULLIF(trim(Matterhyperlink, '#'), '')               AS url
FROM "ftc-ftc-nonmerger-enforcement-actions"
WHERE MatterName IS NOT NULL AND MatterName <> ''
