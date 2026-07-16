-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "LeeftijdVanDeVaderOp31December" AS leeftijdvandevaderop31december,
    "Perioden" AS perioden,
    "LevendgeborenenTotaal_1" AS levendgeborenentotaal_1,
    "Levendgeborenen1eKindUitDeMoeder_2" AS levendgeborenen1ekinduitdemoeder_2,
    "LevendgeborenenTotaal_3" AS levendgeborenentotaal_3,
    "Levendgeborenen1eKindUitDeMoeder_4" AS levendgeborenen1ekinduitdemoeder_4,
    "LeeftijdVanDeVaderOp31December_label" AS leeftijdvandevaderop31december_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-81019ned"
