-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geslacht" AS geslacht,
    "LeeftijdOp31December" AS leeftijdop31december,
    "Geboortegeneratie" AS geboortegeneratie,
    "Sterftekans_1" AS sterftekans_1,
    "LevendenTafelbevolking_2" AS levendentafelbevolking_2,
    "OverledenenTafelbevolking_3" AS overledenentafelbevolking_3,
    "Levensverwachting_4" AS levensverwachting_4,
    "Sterftekans_5" AS sterftekans_5,
    "LevendenTafelbevolking_6" AS levendentafelbevolking_6,
    "OverledenenTafelbevolking_7" AS overledenentafelbevolking_7,
    "Levensverwachting_8" AS levensverwachting_8,
    "Geslacht_label" AS geslacht_label,
    "LeeftijdOp31December_label" AS leeftijdop31december_label,
    "Geboortegeneratie_label" AS geboortegeneratie_label
FROM "cbs-netherlands-80333ned"
