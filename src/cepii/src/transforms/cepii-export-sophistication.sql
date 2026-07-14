-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This legacy workbook combines multiple sophistication measures and source files; filter by source before comparing measure definitions.
SELECT
    "year",
    "country",
    "iso3",
    "Sophistication value of export bundle (EXPY) in US dollars PPP" AS sophistication_value_of_export_bundle_expy_in_us_dollars_ppp,
    "source_file",
    "source_sheet",
    "codeprod",
    "product-level sophistication PRODY for 1997" AS product_level_sophistication_prody_for_1997
FROM "cepii-export-sophistication"
