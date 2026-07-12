-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The workbook restates the full back-series each edition, so historical values should be treated as the latest published CPI series rather than immutable vintages.
SELECT
    "country",
    "iso3",
    "region",
    "year",
    "cpi_score",
    "rank",
    "num_sources",
    "standard_error"
FROM "transparency-international-cpi-timeseries"
