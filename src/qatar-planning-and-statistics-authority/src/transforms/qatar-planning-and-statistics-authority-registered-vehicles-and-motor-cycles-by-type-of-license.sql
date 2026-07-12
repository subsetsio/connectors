-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "government",
    "heavy_equipment_and_machinery",
    "motorcycles",
    "private",
    "private_transport",
    "public_transport",
    "taxis_and_limousines",
    "trailer",
    "other"
FROM "qatar-planning-and-statistics-authority-registered-vehicles-and-motor-cycles-by-type-of-license"
