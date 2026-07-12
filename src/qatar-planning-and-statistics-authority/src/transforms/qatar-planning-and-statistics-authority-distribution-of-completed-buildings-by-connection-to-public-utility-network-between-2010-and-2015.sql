-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "public_utility_network",
    "public_utility_network_ar",
    "connected_census",
    "connected",
    "unconnected_census",
    "unconnected"
FROM "qatar-planning-and-statistics-authority-distribution-of-completed-buildings-by-connection-to-public-utility-network-between-2010-and-2015"
