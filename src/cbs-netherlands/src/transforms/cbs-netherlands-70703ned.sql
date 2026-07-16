-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Perioden" AS perioden,
    "JongensEnMeisjes_1" AS jongensenmeisjes_1,
    "Jongens_2" AS jongens_2,
    "Meisjes_3" AS meisjes_3,
    "MannenEnVrouwen_4" AS mannenenvrouwen_4,
    "Mannen_5" AS mannen_5,
    "Vrouwen_6" AS vrouwen_6,
    "TotaalHuwelijken_7" AS totaalhuwelijken_7,
    "TussenManEnVrouw_8" AS tussenmanenvrouw_8,
    "TussenMannen_9" AS tussenmannen_9,
    "TussenVrouwen_10" AS tussenvrouwen_10,
    "TotaalPartnerschappen_11" AS totaalpartnerschappen_11,
    "TussenManEnVrouw_12" AS tussenmanenvrouw_12,
    "TussenMannen_13" AS tussenmannen_13,
    "TussenVrouwen_14" AS tussenvrouwen_14,
    "EchtScheidingen_15" AS echtscheidingen_15,
    "TotaalVerhuisdePersonen_16" AS totaalverhuisdepersonen_16,
    "BinnenGemeentenVerhuisdePersonen_17" AS binnengemeentenverhuisdepersonen_17,
    "TussenGemeentenVerhuisdePersonen_18" AS tussengemeentenverhuisdepersonen_18,
    "Immigratie_19" AS immigratie_19,
    "EmigratieExclusiefAdministratieveC_20" AS emigratieexclusiefadministratievec_20,
    "Nationaliteitswijzigingen_21" AS nationaliteitswijzigingen_21,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-70703ned"
