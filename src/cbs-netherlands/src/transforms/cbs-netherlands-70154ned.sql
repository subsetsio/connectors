-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "MethodenVanSlibontwatering" AS methodenvanslibontwatering,
    "Perioden" AS perioden,
    "VoorOntwatering_1" AS voorontwatering_1,
    "NaOntwatering_2" AS naontwatering_2,
    "DrogeStofNaOntwatering_3" AS drogestofnaontwatering_3,
    "IngaandRekenkundig_4" AS ingaandrekenkundig_4,
    "UitgaandRekenkundig_5" AS uitgaandrekenkundig_5,
    "IngaandLandelijk_6" AS ingaandlandelijk_6,
    "UitgaandLandelijk_7" AS uitgaandlandelijk_7,
    "MethodenVanSlibontwatering_label" AS methodenvanslibontwatering_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-70154ned"
