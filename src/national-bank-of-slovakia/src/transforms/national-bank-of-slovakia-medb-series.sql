SELECT
    CAST(timeseries_id   AS VARCHAR) AS timeseries_id,
    CAST(name_en         AS VARCHAR) AS name_en,
    CAST(name_sk         AS VARCHAR) AS name_sk,
    CAST(detail          AS VARCHAR) AS detail,
    CAST(source          AS VARCHAR) AS source,
    CAST(subarea_id      AS VARCHAR) AS subarea_id,
    CAST(subarea_en      AS VARCHAR) AS subarea_en,
    CAST(area_id         AS VARCHAR) AS area_id,
    CAST(area_en         AS VARCHAR) AS area_en,
    CAST(macrosector_id  AS VARCHAR) AS macrosector_id,
    CAST(macrosector_en  AS VARCHAR) AS macrosector_en
FROM "national-bank-of-slovakia-medb-series"
