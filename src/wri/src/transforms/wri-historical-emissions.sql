-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains multiple upstream data sources and both country and aggregate geographies; filter `data_source`, `sector`, `gas`, and geography before summing or comparing values.
SELECT
    "iso_code3",
    "country",
    "data_source",
    "sector",
    "gas",
    "unit",
    "year",
    "value"
FROM "wri-historical-emissions"
