SELECT
    country,
    CAST(date AS DATE)              AS date,
    v4_prefixes_ris,
    v6_prefixes_ris,
    asns_ris,
    NULLIF(v4_prefixes_stats, -1)   AS v4_prefixes_stats,
    NULLIF(v6_prefixes_stats, -1)   AS v6_prefixes_stats,
    NULLIF(asns_stats, -1)          AS asns_stats
FROM "ripe-ncc-country-resource-stats"
WHERE date IS NOT NULL
