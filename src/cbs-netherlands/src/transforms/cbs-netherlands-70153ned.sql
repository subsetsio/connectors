-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "KenmerkenInstallaties" AS kenmerkeninstallaties,
    "Perioden" AS perioden,
    "PerKgVerwijderdeBZVRekenkundig_1" AS perkgverwijderdebzvrekenkundig_1,
    "PerKgVerwijderdeBZVLandelijk_2" AS perkgverwijderdebzvlandelijk_2,
    "PerIEAangevoerdRekenkundig_3" AS perieaangevoerdrekenkundig_3,
    "PerIEAangevoerdLandelijk_4" AS perieaangevoerdlandelijk_4,
    "InstallatiesMetWarmeSlibgisting_5" AS installatiesmetwarmeslibgisting_5,
    "CapaciteitMetWarmeSlibgisting_6" AS capaciteitmetwarmeslibgisting_6,
    "AsgehalteInAanvoer_7" AS asgehalteinaanvoer_7,
    "Gistingstemperatuur_8" AS gistingstemperatuur_8,
    "Verblijftijd_9" AS verblijftijd_9,
    "RendementDrogeStofVerwijdering_10" AS rendementdrogestofverwijdering_10,
    "RendementOrganischeStofVerwijdering_11" AS rendementorganischestofverwijdering_11,
    "BiogasproductiePerAangevoerdeKgDS_12" AS biogasproductieperaangevoerdekgds_12,
    "BiogasproductiePerVerwijderdeKgDS_13" AS biogasproductieperverwijderdekgds_13,
    "KenmerkenInstallaties_label" AS kenmerkeninstallaties_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-70153ned"
