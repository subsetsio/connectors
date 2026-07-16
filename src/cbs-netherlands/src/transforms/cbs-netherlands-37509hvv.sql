-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Perioden" AS perioden,
    "TotaalVervoerdGewicht_1" AS totaalvervoerdgewicht_1,
    "RuweAardolieNaarBelgie_2" AS ruweaardolienaarbelgie_2,
    "RuweAardolieNaarDuitsland_3" AS ruweaardolienaarduitsland_3,
    "AardolieproductenNaarDuitsland_4" AS aardolieproductennaarduitsland_4,
    "TotaleVervoersprestatie_5" AS totalevervoersprestatie_5,
    "RuweAardolie_6" AS ruweaardolie_6,
    "Aardolieproducten_7" AS aardolieproducten_7,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-37509hvv"
