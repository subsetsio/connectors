-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `imputation_type` distinguishes two parallel estimates of the same observation — pin it before comparing across states or years.
-- caution: Long-format indicator table: a dimension column is NULL when the row is not disaggregated along that dimension (the row is a total over it). Never aggregate `value` across rows without pinning every dimension column — totals and their components coexist.
SELECT
    "year",
    "state",
    "indicator",
    "sector",
    "imputation_type",
    "value",
    "unit",
    "mpce_fractile_classes",
    "item_category",
    "cereal",
    "employment_of_households",
    "social_group"
FROM "mospi-hces-gethcesrecords"
