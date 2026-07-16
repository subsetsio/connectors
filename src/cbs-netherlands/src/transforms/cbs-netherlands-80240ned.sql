-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "RegioS" AS regios,
    "Perioden" AS perioden,
    "VarkensrechtenInEenheden_1" AS varkensrechtenineenheden_1,
    "VarkensrechtenInFosfaat_2" AS varkensrechteninfosfaat_2,
    "PluimveerechtenInEenheden_3" AS pluimveerechtenineenheden_3,
    "PluimveerechtenInFosfaat_4" AS pluimveerechteninfosfaat_4,
    "VleesEnFokvarkens_5" AS vleesenfokvarkens_5,
    "KippenEnKalkoenen_6" AS kippenenkalkoenen_6,
    "Varkens_7" AS varkens_7,
    "Pluimvee_8" AS pluimvee_8,
    "RegioS_label" AS regios_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80240ned"
