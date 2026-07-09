-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `value` is untyped across rows: what it measures is selected by `datatype_code` and `estimate_code` (cost per hour vs percent of total). Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: `industry_code`, `occupation_code` and `owner_code` each carry 'all' aggregate rows alongside their components.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    "footnote_codes",
    "seasonal",
    "seasonal_name",
    CAST("owner_code" AS BIGINT) AS owner_code,
    "owner_name",
    "industry_code",
    "industry_name",
    "occupation_code",
    "occupation_name",
    "subcell_code",
    "subcell_name",
    "area_code",
    "area_name",
    "datatype_code",
    "datatype_name",
    "estimate_code",
    "estimate_name",
    "series_title"
FROM "bls-cm"
