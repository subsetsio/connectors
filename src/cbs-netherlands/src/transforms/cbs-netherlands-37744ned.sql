-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "LeeftijdVanDeMoeder" AS leeftijdvandemoeder,
    "BurgerlijkeStaatMoeder" AS burgerlijkestaatmoeder,
    "VolgordeGeboorteUitDeMoeder" AS volgordegeboorteuitdemoeder,
    "Perioden" AS perioden,
    "LevendgebLeeftijdMoederOp3112_1" AS levendgebleeftijdmoederop3112_1,
    "LevendgebLftMoederOp3112Rel_2" AS levendgeblftmoederop3112rel_2,
    "LevendgebLftMoederLaatsteVerjDag_3" AS levendgeblftmoederlaatsteverjdag_3,
    "LeeftijdVanDeMoeder_label" AS leeftijdvandemoeder_label,
    "BurgerlijkeStaatMoeder_label" AS burgerlijkestaatmoeder_label,
    "VolgordeGeboorteUitDeMoeder_label" AS volgordegeboorteuitdemoeder_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-37744ned"
