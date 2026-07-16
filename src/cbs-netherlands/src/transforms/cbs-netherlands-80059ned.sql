-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Nationaliteit" AS nationaliteit,
    "Perioden" AS perioden,
    "TotaalAsielverzoekenEnNareizigers_1" AS totaalasielverzoekenennareizigers_1,
    "EersteAsielverzoekenPersonen_2" AS eersteasielverzoekenpersonen_2,
    "VolgendeAsielverzoeken_3" AS volgendeasielverzoeken_3,
    "NareizigersPersonen_4" AS nareizigerspersonen_4,
    "Nationaliteit_label" AS nationaliteit_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80059ned"
