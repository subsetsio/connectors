-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Persoonskenmerken" AS persoonskenmerken,
    "Land" AS land,
    "Perioden" AS perioden,
    "AndereMensen_1" AS anderemensen_1,
    "Rechtssysteem_2" AS rechtssysteem_2,
    "Politie_3" AS politie_3,
    "Politici_4" AS politici_4,
    "Parlement_5" AS parlement_5,
    "PolitiekePartijen_6" AS politiekepartijen_6,
    "EuropeesParlement_7" AS europeesparlement_7,
    "VerenigdeNaties_8" AS verenigdenaties_8,
    "AndereMensen_9" AS anderemensen_9,
    "Rechtssysteem_10" AS rechtssysteem_10,
    "Politie_11" AS politie_11,
    "Politici_12" AS politici_12,
    "Parlement_13" AS parlement_13,
    "PolitiekePartijen_14" AS politiekepartijen_14,
    "EuropeesParlement_15" AS europeesparlement_15,
    "VerenigdeNaties_16" AS verenigdenaties_16,
    "Persoonskenmerken_label" AS persoonskenmerken_label,
    "Land_label" AS land_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80518ned"
