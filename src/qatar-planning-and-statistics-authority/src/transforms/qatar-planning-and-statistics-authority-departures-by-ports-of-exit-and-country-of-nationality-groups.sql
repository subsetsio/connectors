-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "quarter",
    "country_of_nationality_groups",
    "mjmw_t_ldwl",
    "air_port",
    "land_port",
    "sea_port",
    "total"
FROM "qatar-planning-and-statistics-authority-departures-by-ports-of-exit-and-country-of-nationality-groups"
