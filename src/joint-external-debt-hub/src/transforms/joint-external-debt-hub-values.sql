-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Values span multiple debt instruments and countries; filter by series_code or series_name before aggregating across rows.
SELECT
    "country_code",
    "country_name",
    "series_code",
    "series_name",
    "time_label",
    "year",
    "quarter",
    "period_start",
    strptime("source_last_updated", '%Y-%m-%d')::DATE AS source_last_updated,
    "value"
FROM "joint-external-debt-hub-values"
