SELECT
    agreement_id,
    country,
    title_en,
    title_native,
    bargaining_level,
    sector,
    TRY_CAST(in_panel AS INTEGER) AS in_panel
FROM "eurofound-collectively-agreed-wages-agreements"
-- real agreement ids look like 'CA-AT-1865'; this also drops the
-- trailing "Applied filters: ..." footer note row in the xlsx sheet.
WHERE agreement_id LIKE 'CA-%'
