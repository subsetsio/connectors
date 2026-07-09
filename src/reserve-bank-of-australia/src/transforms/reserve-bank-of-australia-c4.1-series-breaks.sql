-- provisional transform for accepted RBA asset without a measured raw profile yet
-- Generated from the connector parser schema to unblock the full DAG run; regenerate with compile-transforms after raw lands.
-- caution: Documents discontinuities and classification changes in related RBA statistical series; use as reference context rather than as measured observations.
SELECT
    "series_id",
    COALESCE("series_title", '') AS series_title,
    COALESCE("description", '') AS description,
    "frequency",
    "series_type",
    "units",
    "source",
    "publication_date",
    strptime("obs_date", '%Y-%m-%d')::DATE AS obs_date,
    "dimension_date",
    COALESCE("value_text", '') AS value_text,
    "source_csv",
    "partition_key",
    "record_type",
    COALESCE("break_type", '') AS break_type,
    COALESCE("details", '') AS details
FROM "reserve-bank-of-australia-c4.1-series-breaks"
