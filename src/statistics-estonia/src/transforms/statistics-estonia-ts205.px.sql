-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "reference_period",
    "partner_country",
    "arrival_departure",
    "type_of_flight",
    "indicator",
    "value"
FROM "statistics-estonia-ts205.px"
