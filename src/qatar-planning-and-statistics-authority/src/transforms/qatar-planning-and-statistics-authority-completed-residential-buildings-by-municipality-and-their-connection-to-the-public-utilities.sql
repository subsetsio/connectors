-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "census_year",
    "municipality",
    "lbldy",
    "service",
    "lkhdm",
    "status",
    "lhl",
    "value"
FROM "qatar-planning-and-statistics-authority-completed-residential-buildings-by-municipality-and-their-connection-to-the-public-utilities"
