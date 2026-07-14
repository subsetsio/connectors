-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Dependence indicators are importer-product-year measures; the first origin dependency column is part of the observed row identity.
SELECT
    "iso_d",
    "hs6",
    "year",
    "import_dpt",
    "c1",
    "c2",
    "c3",
    "c4",
    "dependent",
    "sect_agrifood",
    "sect_chemicals",
    "sect_pharmaceuticals",
    "sect_steel",
    "sect_defense",
    "sect_transport",
    "sect_electronics",
    "sect_other",
    "first_odpt",
    "share_odpt"
FROM "cepii-geodep"
