-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geslacht" AS geslacht,
    "LeeftijdOp31December" AS leeftijdop31december,
    "Marges" AS marges,
    "Perioden" AS perioden,
    "LevensverwachtingLV_1" AS levensverwachtinglv_1,
    "LVInAlsGoedErvarenGezondheid_2" AS lvinalsgoedervarengezondheid_2,
    "LVZonderMatigeEnErnstigeBeperking_3" AS lvzondermatigeenernstigebeperking_3,
    "LVZonderErnstigeBeperkingen_4" AS lvzonderernstigebeperkingen_4,
    "LVZonderLichteMatigeErnstigeBep_5" AS lvzonderlichtematigeernstigebep_5,
    "LVZonderChronischeZiektes_6" AS lvzonderchronischeziektes_6,
    "LVZonderChrZiekExclHogeBloeddruk_7" AS lvzonderchrziekexclhogebloeddruk_7,
    "LVZonderPsychischeKlachtenMHI5_8" AS lvzonderpsychischeklachtenmhi5_8,
    "LVZonderGALIBeperkingen_9" AS lvzondergalibeperkingen_9,
    "LVZonderErnstigeGALIBeperkingen_10" AS lvzonderernstigegalibeperkingen_10,
    "Geslacht_label" AS geslacht_label,
    "LeeftijdOp31December_label" AS leeftijdop31december_label,
    "Marges_label" AS marges_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-71950ned"
