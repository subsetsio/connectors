-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "country_of_registration",
    "bld_ltsjyl",
    "number_tonnage",
    "l_dd_wlhmwl",
    "others_khr",
    "passengers_vessels_nqlt_rkb",
    "vehicles_vessels_nqlt_mrkbt",
    "live_sheep_gnm_hy",
    "loose_materials_mwd_sy_b",
    "containers_hwyt",
    "generals_goods_bdy_m",
    "gas_tankers_nqlt_gz",
    "oil_tankers_nqlt_nft"
FROM "qatar-planning-and-statistics-authority-arriving-vessels-gross-and-net-tonnage-by-type-of-vessel-and-country-of-registration-total"
