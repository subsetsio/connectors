-- comex-stat-via: reference/codebook table — trimmed labels, typed codes
SELECT
    "CO_VIA"       AS transport_mode_code,
    TRIM("NO_VIA") AS name_pt
FROM "comex-stat-via"
