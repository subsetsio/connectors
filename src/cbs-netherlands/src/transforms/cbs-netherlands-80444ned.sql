-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Perioden" AS perioden,
    "Prijsindex_1" AS prijsindex_1,
    "MutatiesTovDezelfdePeriodeVorigJaar_2" AS mutatiestovdezelfdeperiodevorigjaar_2,
    "Prijsindex_3" AS prijsindex_3,
    "MutatiesTovDezelfdePeriodeVorigJaar_4" AS mutatiestovdezelfdeperiodevorigjaar_4,
    "Prijsindex_5" AS prijsindex_5,
    "MutatiesTovDezelfdePeriodeVorigJaar_6" AS mutatiestovdezelfdeperiodevorigjaar_6,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80444ned"
