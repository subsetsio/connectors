-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    "year",
    "position",
    "value"
FROM "geostat-gender-20statistics-influence-20and-20power-09-results-of-elections-on-local-authority-mayors-and-governors"
