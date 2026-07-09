-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `value` is untyped across rows: what it measures is selected by `category_code`, `subcategory_code` and `process_code`. Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: `category_code`/`subcategory_code` form an expenditure hierarchy whose parent rows already contain their components.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    CAST("footnote_codes" AS BIGINT) AS footnote_codes,
    "seasonal",
    "category_code",
    "category_name",
    "subcategory_code",
    "item_code",
    "demographics_code",
    "demographics_name",
    "characteristics_code",
    "process_code",
    "process_name",
    "series_title"
FROM "bls-cx"
