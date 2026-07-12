-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "hlpi_name",
    "series_ref",
    "quarter",
    "hlpi",
    "nzhec",
    "nzhec_name",
    "nzhec_short",
    "level",
    CAST("index" AS BIGINT) AS index,
    "change.q" AS change_q,
    "change.a" AS change_a
FROM "statsnz-household-living-costs-price-indexes-march-2026-quarter-time-series-indexes"
