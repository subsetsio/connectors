-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "country_of_previous_port",
    "bld_lmyn_lsbq",
    "vessel_type",
    "nw_lsfyn",
    "indicator",
    "lbyn",
    "number"
FROM "qatar-planning-and-statistics-authority-arriving-vessels-gross-and-net-tonnage-by-type-of-vessel-and-country-of-previous-port"
