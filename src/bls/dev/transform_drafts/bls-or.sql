-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `value` is untyped across rows: what it measures is selected by `datatype_code`, `estimate_code` and `additive_code`. Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: `industry_code` and `occupation_code` each carry 'all' aggregate rows alongside their components.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    "footnote_codes",
    "seasonal",
    "seasonal_name",
    CAST("ownership_code" AS BIGINT) AS ownership_code,
    "ownership_name",
    "industry_code",
    "industry_name",
    "occupation_code",
    "occupation_name",
    "soc_code",
    "job_characteristic_code",
    "job_characteristic_name",
    "estimate_code",
    "estimate_name",
    "datatype_code",
    "datatype_name",
    "category_code",
    "category_name",
    "additive_code",
    "additive_name",
    "requirement_code",
    "requirement_name",
    "series_title"
FROM "bls-or"
