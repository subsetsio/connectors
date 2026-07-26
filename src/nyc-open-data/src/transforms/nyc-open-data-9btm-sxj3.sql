-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "location_category",
    "administrative_district",
    "gen_ed_removals",
    "gen_ed_principal",
    "gen_ed_superintendent",
    "gen_ed_expulsions",
    "swd_removals",
    "swd_principal",
    "swd_superintendent",
    "swd_expulsions"
FROM "nyc-open-data-9btm-sxj3"
