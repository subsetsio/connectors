-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geslacht" AS geslacht,
    "Leeftijd" AS leeftijd,
    "BurgerlijkeStaat" AS burgerlijkestaat,
    "Perioden" AS perioden,
    "Bevolking_1" AS bevolking_1,
    "Geslacht_label" AS geslacht_label,
    "Leeftijd_label" AS leeftijd_label,
    "BurgerlijkeStaat_label" AS burgerlijkestaat_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-7461bev"
