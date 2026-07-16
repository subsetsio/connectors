-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Perioden" AS perioden,
    "TotaleLuchtvloot_1" AS totaleluchtvloot_1,
    "TotaalVleugelvliegtuigen_2" AS totaalvleugelvliegtuigen_2,
    "TotaalStraalmotoren_3" AS totaalstraalmotoren_3,
    "k_4Motorig_4" AS k_4motorig_4,
    "k_3Motorig_5" AS k_3motorig_5,
    "k_2Motorig_6" AS k_2motorig_6,
    "k_1Motorig_7" AS k_1motorig_7,
    "TotaalSchroefturbinemotoren_8" AS totaalschroefturbinemotoren_8,
    "k_4Motorig_9" AS k_4motorig_9,
    "k_3Motorig_10" AS k_3motorig_10,
    "k_2Motorig_11" AS k_2motorig_11,
    "k_1Motorig_12" AS k_1motorig_12,
    "TotaalZuigermotoren_13" AS totaalzuigermotoren_13,
    "k_4Motorig_14" AS k_4motorig_14,
    "k_2Motorig_15" AS k_2motorig_15,
    "k_1Motorig_16" AS k_1motorig_16,
    "TotaalUltraLightS_17" AS totaalultralights_17,
    "VeryLightVLA_18" AS verylightvla_18,
    "MicroLightMLA_19" AS microlightmla_19,
    "TotaalZweefvliegtuigen_20" AS totaalzweefvliegtuigen_20,
    "k_1Motorig_21" AS k_1motorig_21,
    "GeenMotor_22" AS geenmotor_22,
    "TotaalHefschroefvliegtuigen_23" AS totaalhefschroefvliegtuigen_23,
    "k_2Motorig_24" AS k_2motorig_24,
    "k_1Motorig_25" AS k_1motorig_25,
    "Ballonvaartuigen_26" AS ballonvaartuigen_26,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-37721hvv"
