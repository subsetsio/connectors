-- comex-stat-nbm: reference/codebook table — trimmed labels, typed codes
SELECT
    "CO_NBM"       AS nbm_code,
    TRIM("NO_NBM") AS name_pt
FROM "comex-stat-nbm"
