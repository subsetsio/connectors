-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "lshhr",
    "public_transport_buses",
    "doha_metro",
    "lusail_tram"
FROM "qatar-planning-and-statistics-authority-public-transport-users"
