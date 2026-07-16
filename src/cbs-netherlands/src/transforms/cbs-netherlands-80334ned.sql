-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Perioden" AS perioden,
    "Index_1" AS index_1,
    "MutatiesTovDezelfdePeriodeVorigJaar_2" AS mutatiestovdezelfdeperiodevorigjaar_2,
    "Index_3" AS index_3,
    "MutatiesTovDezelfdePeriodeVorigJaar_4" AS mutatiestovdezelfdeperiodevorigjaar_4,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80334ned"
