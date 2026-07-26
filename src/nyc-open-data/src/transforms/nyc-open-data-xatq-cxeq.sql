-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "reference_year",
    "economic_indicator",
    "unit",
    "forecast_value",
    "revision_reason"
FROM "nyc-open-data-xatq-cxeq"
