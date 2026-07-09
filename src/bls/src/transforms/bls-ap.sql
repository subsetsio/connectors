-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `value` is untyped across rows: what it measures is selected by `item_code` (which good or service) and `area_code` (which market). Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: `area_code` carries the 'U.S. city average' (0000) aggregate alongside regions and individual metro areas; `value` is an average price, so it must never be summed and may only be averaged within one `item_code` + `area_code`.
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
    "series_title"
FROM "bls-ap"
