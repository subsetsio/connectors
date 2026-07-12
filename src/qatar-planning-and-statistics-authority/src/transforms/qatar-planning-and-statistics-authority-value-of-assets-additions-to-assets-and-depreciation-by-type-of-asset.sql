-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_asset",
    "category",
    "value_of_assets_at_end_of_the_year",
    "depreciation_during_the_year",
    "omissions_during_the_year",
    "additions_during_the_year",
    "value_of_assets_at_beginning_of_the_year",
    "category_ar",
    "type_of_asset_ar"
FROM "qatar-planning-and-statistics-authority-value-of-assets-additions-to-assets-and-depreciation-by-type-of-asset"
