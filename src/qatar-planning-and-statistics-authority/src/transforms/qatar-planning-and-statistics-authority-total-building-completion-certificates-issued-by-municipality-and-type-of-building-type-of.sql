-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "building_type",
    "nw_lmbn",
    "certificate_type",
    "nw_lshhd",
    "municipality",
    "lbldy",
    "count"
FROM "qatar-planning-and-statistics-authority-total-building-completion-certificates-issued-by-municipality-and-type-of-building-type-of"
