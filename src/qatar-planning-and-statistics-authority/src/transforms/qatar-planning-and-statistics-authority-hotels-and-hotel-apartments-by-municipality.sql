-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "municipality",
    "lbldy",
    "facility_type",
    "nw_lmnsh",
    "number"
FROM "qatar-planning-and-statistics-authority-hotels-and-hotel-apartments-by-municipality"
