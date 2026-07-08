SELECT
    incident_id                              AS incident_id,
    fire_name                                AS fire_name,
    UniqueFireIdentifier                     AS unique_fire_id,
    IrwinID                                  AS irwin_id,
    TRY_CAST(latitude AS DOUBLE)             AS latitude,
    TRY_CAST(longitude AS DOUBLE)            AS longitude,
    TRY_CAST(size AS DOUBLE)                 AS size_acres,
    gacc                                     AS gacc,
    imt_type                                 AS imt_type,
    x100pct                                  AS contained_flag,
    CASE WHEN epoch_ms(TRY_CAST(initial_imsr_date AS BIGINT)) BETWEEN TIMESTAMP '1900-01-01' AND TIMESTAMP '2027-12-31' THEN epoch_ms(TRY_CAST(initial_imsr_date AS BIGINT)) END               AS initial_imsr_at,
    CASE WHEN epoch_ms(TRY_CAST(intl_imsr_post_date AS BIGINT)) BETWEEN TIMESTAMP '1900-01-01' AND TIMESTAMP '2027-12-31' THEN epoch_ms(TRY_CAST(intl_imsr_post_date AS BIGINT)) END             AS intl_imsr_post_at,
    post_year                                AS post_year,
    post_month                               AS post_month,
    Occurrence                               AS occurrence,
    TRY_CAST(nmbr_apprs AS INTEGER)          AS num_appearances
FROM "nifc-eaa333df1850483abdd0465f86212e03-0"
