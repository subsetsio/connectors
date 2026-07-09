-- provisional transform for accepted RBA asset without a measured raw profile yet
-- Generated from the connector parser schema to unblock the full DAG run; regenerate with compile-transforms after raw lands.
-- caution: Rows are the source statistical table in long form; series metadata columns identify the measure and unit, and value_text preserves non-numeric source cells.
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
FROM "reserve-bank-of-australia-a3-omo-repo-transaction-details"
