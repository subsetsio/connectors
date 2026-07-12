-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "building_type",
    "nw_lmbn",
    "permit_type",
    "nw_lrkhs",
    "municipality",
    "lbldy",
    "count"
FROM "qatar-planning-and-statistics-authority-total-building-permits-issued-by-municipality-and-type-of-building-type-of-permit"
