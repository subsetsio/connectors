-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `period` mixes regular observations with BLS aggregate period codes — M13 (annual average). `period_start_date` is derived as the first day of the observation period, so an aggregate row lands on the same date as the year's first regular row (M13/S01/S03/A01 and Q05 all stamp January 1). Filter on `period` — grouping or summing by `period_start_date` alone double-counts.
-- caution: `value` is untyped across rows: what it measures is selected by `item_code`, `area_code` and `base_code`/`base_period` (the index reference base). Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: `item_code` is a hierarchy and `area_code` carries the 'U.S. city average' aggregate alongside sub-national areas; do not sum across either.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    "footnote_codes",
    "area_code",
    "area_name",
    "item_code",
    "item_name",
    "seasonal",
    "seasonal_name",
    "periodicity_code",
    "periodicity_name",
    "base_code",
    "base_name",
    "base_period",
    "series_title"
FROM "bls-su"
