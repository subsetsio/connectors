-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "public_transport_buses_fleet",
    "number_of_electric_buses",
    "percentage_of_electric_buses"
FROM "qatar-planning-and-statistics-authority-percentage-of-electric-buses-in-the-public-transport-fleet"
