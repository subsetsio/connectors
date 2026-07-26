-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "enumber",
    "borocode",
    "taxblock",
    "taxlot",
    "ceqr_num",
    "ulurp_num",
    "zoning_map",
    "descriptio",
    "bbl",
    "geometry"
FROM "nyc-open-data-jsrs-ggnx"
