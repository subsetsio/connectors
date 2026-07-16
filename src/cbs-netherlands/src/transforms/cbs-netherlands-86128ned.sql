-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Leeftijd" AS leeftijd,
    "Huishoudenskenmerken" AS huishoudenskenmerken,
    "Perioden" AS perioden,
    "KinderenTotaal_1" AS kinderentotaal_1,
    "KinderenArm_2" AS kinderenarm_2,
    "KinderenLangdurigArm_3" AS kinderenlangdurigarm_3,
    "KinderenArmRelatief_4" AS kinderenarmrelatief_4,
    "KinderenLangdurigArmRelatief_5" AS kinderenlangdurigarmrelatief_5,
    "Leeftijd_label" AS leeftijd_label,
    "Huishoudenskenmerken_label" AS huishoudenskenmerken_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-86128ned"
