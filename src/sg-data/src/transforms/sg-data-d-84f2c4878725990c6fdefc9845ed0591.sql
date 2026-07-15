-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_name",
    "area",
    "type_of_stall",
    "remarks",
    "closing_on",
    "detailed_requirements"
FROM "sg-data-d-84f2c4878725990c6fdefc9845ed0591"
