-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "BalanspostenGemeenten" AS balanspostengemeenten,
    "Regiokenmerken" AS regiokenmerken,
    "Perioden" AS perioden,
    "BalansstandenUltimoInMlnEuro_1" AS balansstandenultimoinmlneuro_1,
    "BalansstandenUltimoInEuroInwoner_2" AS balansstandenultimoineuroinwoner_2,
    "BalanspostenGemeenten_label" AS balanspostengemeenten_label,
    "Regiokenmerken_label" AS regiokenmerken_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-71231ned"
