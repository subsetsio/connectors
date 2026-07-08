SELECT
    TRY_CAST(MatterEnforcementFY AS INTEGER)              AS enforcement_fy,
    TRY_STRPTIME(MatterEnforcementDate, '%m/%d/%Y %H:%M')::DATE AS enforcement_date,
    MatterName                                           AS matter_name,
    MatterNumber                                         AS matter_number,
    MatterEnforcementType                                AS enforcement_type,
    MatterType                                           AS matter_type,
    NULLIF(trim(Matterhyperlink, '#'), '')               AS url
FROM "ftc-ftc-civil-penalty-actions"
WHERE MatterName IS NOT NULL AND MatterName <> ''
