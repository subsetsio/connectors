-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "VakcentralesEnVakverenigingen" AS vakcentralesenvakverenigingen,
    "Geslacht" AS geslacht,
    "Leeftijd" AS leeftijd,
    "Perioden" AS perioden,
    "Leden_1" AS leden_1,
    "LedenRelatief_2" AS ledenrelatief_2,
    "VakcentralesEnVakverenigingen_label" AS vakcentralesenvakverenigingen_label,
    "Geslacht_label" AS geslacht_label,
    "Leeftijd_label" AS leeftijd_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80598ned"
