-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_license",
    "nw_ltrkhys",
    "total"
FROM "qatar-planning-and-statistics-authority-registered-new-vehicles-and-motor-cycles-by-type-of-license"
