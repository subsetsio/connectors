SELECT company,
       refinery,
       state,
       CAST(capacity AS DOUBLE) AS capacity_kt,
       TRY_CAST(as_of AS DATE) AS as_of,
       unit
FROM "ppac-infrastructure-installed-refinery-capacity"
WHERE refinery IS NOT NULL AND capacity IS NOT NULL
