SELECT
    TRY_CAST(asOfDate AS DATE)           AS as_of_date,
    TRY_CAST(bills AS DOUBLE)            AS bills,
    TRY_CAST(notesbonds AS DOUBLE)      AS notes_bonds,
    TRY_CAST(tips AS DOUBLE)            AS tips,
    TRY_CAST(frn AS DOUBLE)             AS frn,
    TRY_CAST(tipsInflationCompensation AS DOUBLE) AS tips_inflation_compensation,
    TRY_CAST(mbs AS DOUBLE)            AS mbs,
    TRY_CAST(cmbs AS DOUBLE)           AS cmbs,
    TRY_CAST(agencies AS DOUBLE)       AS agencies,
    TRY_CAST(total AS DOUBLE)          AS total
FROM "ny-fed-soma-summary"
WHERE TRY_CAST(asOfDate AS DATE) IS NOT NULL
