-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "AantalPersonen" AS aantalpersonen,
    "Perioden" AS perioden,
    "TotaalParticuliereHuishoudens_1" AS totaalparticulierehuishoudens_1,
    "Eenpersoonshuishoudens_2" AS eenpersoonshuishoudens_2,
    "TotaalMeerpersoonshuishoudens_3" AS totaalmeerpersoonshuishoudens_3,
    "MeerpersoonshuishoudensZonderKinderen_4" AS meerpersoonshuishoudenszonderkinderen_4,
    "MeerpersoonshuishoudensMetKinderen_5" AS meerpersoonshuishoudensmetkinderen_5,
    "NietGehuwdPaarZonderKinderen_6" AS nietgehuwdpaarzonderkinderen_6,
    "NietGehuwdPaarMetKinderen_7" AS nietgehuwdpaarmetkinderen_7,
    "GehuwdPaarZonderKinderen_8" AS gehuwdpaarzonderkinderen_8,
    "GehuwdPaarMetKinderen_9" AS gehuwdpaarmetkinderen_9,
    "Eenouderhuishouden_10" AS eenouderhuishouden_10,
    "OverigHuishouden_11" AS overighuishouden_11,
    "AantalPersonen_label" AS aantalpersonen_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-70133ned"
