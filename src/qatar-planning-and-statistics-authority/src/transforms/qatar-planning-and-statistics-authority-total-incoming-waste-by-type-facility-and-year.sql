-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "incoming_waste",
    "total_value"
FROM "qatar-planning-and-statistics-authority-total-incoming-waste-by-type-facility-and-year"
