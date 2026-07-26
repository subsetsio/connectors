-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_program" AS program,
    "category",
    "agency_that_provides_service",
    "description",
    "geographical_unit_covered"
FROM "nyc-open-data-p2vv-pesb"
