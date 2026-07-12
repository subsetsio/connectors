-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "station",
    "lmht",
    "rented_by_kahramaa",
    "municipality",
    "education",
    "defense",
    "police",
    "other",
    "rural_tankers",
    "private_transport"
FROM "qatar-planning-and-statistics-authority-tanker-water-supply-by-station-2023"
