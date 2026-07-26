-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "enumber",
    "e_effective_date",
    "borocode",
    "taxblock",
    "taxlot",
    "hazmat_code",
    "air_code",
    "noise_code",
    "hazmat_date",
    "air_date",
    "noise_date",
    "ceqr_num",
    "ulurp_num",
    "zoning_map",
    "description",
    "bbl"
FROM "nyc-open-data-hxm3-23vy"
