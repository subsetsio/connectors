SELECT
    mnemonic, dataset, monitor, name, subtype,
    frequency, unit_type, unit_name,
    TRY_CAST(NULLIF(start_date, '') AS DATE) AS start_date
FROM "ofr-ofr-series-catalog"
WHERE mnemonic IS NOT NULL
