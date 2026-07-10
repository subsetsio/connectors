-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are normalized from RBA CSV files into long form; series metadata columns identify the measure and unit, and value_text preserves non-numeric source cells alongside the numeric transform value where parseable.
SELECT
    "series_id",
    "series_title",
    "description",
    "frequency",
    "series_type",
    "units",
    "source",
    "publication_date",
    strptime("obs_date", '%Y-%m-%d')::DATE AS obs_date,
    "dimension_date",
    CAST("value_text" AS BIGINT) AS value_text,
    "source_csv",
    "partition_key",
    "record_type",
    "break_type",
    "details"
FROM "reserve-bank-of-australia-a6-data-prior-to-1984"
