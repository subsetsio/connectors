-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are source reference/event annotations for related RBA statistical series rather than primary observations; use them to interpret breaks, judgement notes, or other table-specific metadata.
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
    "value_text",
    "source_csv",
    "partition_key",
    "record_type",
    "break_type",
    "details"
FROM "reserve-bank-of-australia-b13.1.2-series-breaks"
