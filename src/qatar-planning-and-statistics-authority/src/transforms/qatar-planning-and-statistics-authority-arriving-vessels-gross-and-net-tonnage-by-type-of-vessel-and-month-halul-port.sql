-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "month",
    "number_tonnage",
    "l_dd_wlhmwl",
    "lshhr",
    "total",
    "others",
    "passengers_vessel",
    "vehicles_vessels",
    "live_sheep",
    "loose_materials",
    "containers",
    "generals_goods",
    "gas_tankers",
    "oil_tankers"
FROM "qatar-planning-and-statistics-authority-arriving-vessels-gross-and-net-tonnage-by-type-of-vessel-and-month-halul-port"
