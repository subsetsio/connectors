-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "gcc_nationality",
    "nationality_ar",
    "value"
FROM "qatar-planning-and-statistics-authority-gcc-citizens-in-qatars-retirement-scheme-private-sector"
