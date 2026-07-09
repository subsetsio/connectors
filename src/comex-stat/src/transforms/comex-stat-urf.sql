-- comex-stat-urf: reference/codebook table — trimmed labels, typed codes
SELECT
    "CO_URF"       AS customs_unit_code,
    TRIM("NO_URF") AS name_pt
FROM "comex-stat-urf"
