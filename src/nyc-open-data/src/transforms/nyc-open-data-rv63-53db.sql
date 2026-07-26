-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "section",
    "frequency",
    "schedulecode",
    "freq_refuse",
    "freq_recycling",
    "freq_organics",
    "freq_bulk",
    "objectid",
    "shape_area",
    "shape_length",
    "multipolygon",
    "freq_ewaste",
    "freq_resfuseid"
FROM "nyc-open-data-rv63-53db"
