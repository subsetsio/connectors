-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reference_period",
    "seasonal_adjustment",
    "type_of_construction",
    "place_of_construction_activity",
    "indicator",
    "value"
FROM "statistics-estonia-eh0014.px"
