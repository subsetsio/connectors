-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "use",
    "sex",
    "year",
    "frequency",
    "value"
FROM "geostat-gender-20statistics-ict-01-distribution-of-population-aged-15-and-older-by-frequency-of-computer"
