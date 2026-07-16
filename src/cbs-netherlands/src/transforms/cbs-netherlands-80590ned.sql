-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geslacht" AS geslacht,
    "Leeftijd" AS leeftijd,
    "Perioden" AS perioden,
    "NietSeizoengecorrigeerd_1" AS nietseizoengecorrigeerd_1,
    "Seizoengecorrigeerd_2" AS seizoengecorrigeerd_2,
    "NietSeizoengecorrigeerd_3" AS nietseizoengecorrigeerd_3,
    "Seizoengecorrigeerd_4" AS seizoengecorrigeerd_4,
    "NietSeizoengecorrigeerd_5" AS nietseizoengecorrigeerd_5,
    "Seizoengecorrigeerd_6" AS seizoengecorrigeerd_6,
    "NietSeizoengecorrigeerd_7" AS nietseizoengecorrigeerd_7,
    "Seizoengecorrigeerd_8" AS seizoengecorrigeerd_8,
    "NietSeizoengecorrigeerd_9" AS nietseizoengecorrigeerd_9,
    "Seizoengecorrigeerd_10" AS seizoengecorrigeerd_10,
    "NietSeizoengecorrigeerd_11" AS nietseizoengecorrigeerd_11,
    "Seizoengecorrigeerd_12" AS seizoengecorrigeerd_12,
    "NietSeizoengecorrigeerd_13" AS nietseizoengecorrigeerd_13,
    "Seizoengecorrigeerd_14" AS seizoengecorrigeerd_14,
    "Geslacht_label" AS geslacht_label,
    "Leeftijd_label" AS leeftijd_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80590ned"
