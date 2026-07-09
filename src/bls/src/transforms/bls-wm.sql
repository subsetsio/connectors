-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `value` is untyped across rows: what it measures is selected by `datatype_code`, `estimate_code` and `level_code`. Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: `industry_code`, `occupation_code` and `ownership_code` each carry 'all' aggregate rows alongside their components.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    "footnote_codes",
    "seasonal",
    "seasonal_name",
    "area_code",
    "area_name",
    CAST("ownership_code" AS BIGINT) AS ownership_code,
    "ownership_name",
    "estimate_code",
    "estimate_name",
    "industry_code",
    "industry_name",
    CAST("occupation_code" AS BIGINT) AS occupation_code,
    "occupation_name",
    "subcell_code",
    "subcell_name",
    CAST("datatype_code" AS BIGINT) AS datatype_code,
    "datatype_name",
    "level_code",
    "level_name",
    "series_title"
FROM "bls-wm"
