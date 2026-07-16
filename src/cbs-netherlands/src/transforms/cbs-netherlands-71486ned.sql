-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "LeeftijdReferentiepersoon" AS leeftijdreferentiepersoon,
    "RegioS" AS regios,
    "Perioden" AS perioden,
    "TotaalParticuliereHuishoudens_1" AS totaalparticulierehuishoudens_1,
    "Eenpersoonshuishouden_2" AS eenpersoonshuishouden_2,
    "TotaalMeerpersoonshuishoudens_3" AS totaalmeerpersoonshuishoudens_3,
    "MeerpersoonshuishoudensZonderKinderen_4" AS meerpersoonshuishoudenszonderkinderen_4,
    "MeerpersoonshuishoudensMetKinderen_5" AS meerpersoonshuishoudensmetkinderen_5,
    "TotaalNietGehuwdeParen_6" AS totaalnietgehuwdeparen_6,
    "k_0Kinderen_7" AS k_0kinderen_7,
    "k_1Kind_8" AS k_1kind_8,
    "k_2Kinderen_9" AS k_2kinderen_9,
    "k_3OfMeerKinderen_10" AS k_3ofmeerkinderen_10,
    "TotaalGehuwdeParen_11" AS totaalgehuwdeparen_11,
    "k_0Kinderen_12" AS k_0kinderen_12,
    "k_1Kind_13" AS k_1kind_13,
    "k_2Kinderen_14" AS k_2kinderen_14,
    "k_3OfMeerKinderen_15" AS k_3ofmeerkinderen_15,
    "TotaalEenouderhuishoudens_16" AS totaaleenouderhuishoudens_16,
    "k_1Kind_17" AS k_1kind_17,
    "k_2Kinderen_18" AS k_2kinderen_18,
    "k_3OfMeerKinderen_19" AS k_3ofmeerkinderen_19,
    "OverigHuishouden_20" AS overighuishouden_20,
    "TotaalParticuliereHuishoudens_21" AS totaalparticulierehuishoudens_21,
    "Eenpersoonshuishouden_22" AS eenpersoonshuishouden_22,
    "TotaalMeerpersoonshuishoudens_23" AS totaalmeerpersoonshuishoudens_23,
    "k_2Personen_24" AS k_2personen_24,
    "k_3Personen_25" AS k_3personen_25,
    "k_4Personen_26" AS k_4personen_26,
    "k_5OfMeerPersonen_27" AS k_5ofmeerpersonen_27,
    "LeeftijdReferentiepersoon_label" AS leeftijdreferentiepersoon_label,
    "RegioS_label" AS regios_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-71486ned"
