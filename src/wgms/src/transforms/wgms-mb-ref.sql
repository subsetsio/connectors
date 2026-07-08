SELECT
    TRY_CAST("Year" AS INTEGER)         AS year,
    TRY_CAST(MB_REF_count AS INTEGER)   AS reference_glacier_count,
    TRY_CAST(REF_regionAVG AS DOUBLE)   AS annual_mass_balance_mm_we,
    TRY_CAST("REF_regionAVG_cum-rel-1970" AS DOUBLE)
                                        AS cumulative_mass_balance_mm_we_rel_1970
FROM "wgms-mb-ref"
WHERE TRY_CAST("Year" AS INTEGER) IS NOT NULL
