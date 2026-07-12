-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reference_period",
    "type_of_residential_building",
    "county",
    "type_of_permit",
    "type_of_construction",
    "indicator",
    "value"
FROM "statistics-estonia-eh045.px"
