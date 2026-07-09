-- comex-stat-ncm-fat-agreg: reference/codebook table — trimmed labels, typed codes
SELECT
    "CO_FAT_AGREG"          AS factor_aggregate_code,
    TRIM("NO_FAT_AGREG")    AS name_pt,
    TRIM("NO_FAT_AGREG_GP") AS group_name_pt
FROM "comex-stat-ncm-fat-agreg"
