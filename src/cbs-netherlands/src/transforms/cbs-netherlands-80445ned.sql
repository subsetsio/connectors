-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "BalansstandenWaterschappen" AS balansstandenwaterschappen,
    "Waterschappen" AS waterschappen,
    "Perioden" AS perioden,
    "BalansstandenUltimo_1" AS balansstandenultimo_1,
    "BalansstandenWaterschappen_label" AS balansstandenwaterschappen_label,
    "Waterschappen_label" AS waterschappen_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80445ned"
