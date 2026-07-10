SELECT
    TRIM("TYPE-COLLATERAL") AS type_collateral,
    TRIM("COLLATERAL") AS collateral,
    TRIM("PARTY") AS party,
    TRIM("DOC-ID") AS doc_id,
    TRY_STRPTIME(NULLIF(TRIM("DRDATE"), ''), '%Y%m%d')::DATE AS dr_date,
    TRY_STRPTIME(NULLIF(TRIM("PROCESSING-DATE"), ''), '%Y%m%d')::DATE AS processing_date,
    TRY_STRPTIME(NULLIF(TRIM("CORR-DATE"), ''), '%Y%m%d')::DATE AS corr_date,
    TRIM("CORR-ID") AS corr_id,
    TRIM("SERIAL-ID") AS serial_id,
    TRIM("DOC-TYPE") AS doc_type
FROM "faa-docindex"
WHERE TRIM("DOC-ID") <> ''
