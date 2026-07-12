-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The catalog mixes interest-rate, yield, and exchange-rate series; use the description and group columns to select comparable measures before comparing or aggregating series.
SELECT
    "series_id",
    "source",
    "short_description",
    "mid_description",
    "long_description",
    "group_id",
    strptime("observation_min_date", '%Y-%m-%d')::DATE AS observation_min_date,
    strptime("observation_max_date", '%Y-%m-%d')::DATE AS observation_max_date,
    "series_closed"
FROM "sveriges-riksbank-series"
