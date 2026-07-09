-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `value` is untyped across rows: what it measures is selected by `measure_type_code`, `measure_unit_code` and `measure_multiplier_code`. Never aggregate `value` without first pinning those dimensions to a single measure.
-- caution: Demographic dimension codes carry 'all'/'total' rows alongside their breakdowns.
-- caution: `value` must be scaled by `measure_multiplier_code` before it is comparable across series.
SELECT
    "series_id",
    "year",
    "period",
    "period_start_date",
    "value",
    CAST("footnote_codes" AS BIGINT) AS footnote_codes,
    "seasonal",
    "measure_type_code",
    "measure_unit_code",
    "measure_multiplier_code",
    "publication_flag",
    "lfst_code",
    "lfst_name",
    "series_title",
    "ages_code",
    "ages_name",
    "clas_code",
    "clas_name",
    "indy_code",
    "indy_name",
    "pcts_code",
    "pcts_name",
    "rsng_code",
    "rsng_name",
    "scdr_code",
    "scdr_name",
    CAST("sexs_code" AS BIGINT) AS sexs_code,
    "sexs_name",
    "tdat_code",
    "tdat_name",
    "vets_code",
    "vets_name"
FROM "bls-kv"
