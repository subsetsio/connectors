-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sample_id",
    "sample_date",
    "beach_name",
    "sample_location",
    "enterococci_results",
    "units_or_notes"
FROM "nyc-open-data-2xir-kwzz"
