-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geslacht" AS geslacht,
    "RegioS" AS regios,
    "Perioden" AS perioden,
    "BevolkingOp1Januari_1" AS bevolkingop1januari_1,
    "Bevolkingsdichtheid_2" AS bevolkingsdichtheid_2,
    "LevendGeborenKinderen_3" AS levendgeborenkinderen_3,
    "LevendGeborenKinderenRelatief_4" AS levendgeborenkinderenrelatief_4,
    "Overledenen_5" AS overledenen_5,
    "OverledenenRelatief_6" AS overledenenrelatief_6,
    "Geboorteoverschot_7" AS geboorteoverschot_7,
    "TotaalVestiging_8" AS totaalvestiging_8,
    "TotaalVestigingRelatief_9" AS totaalvestigingrelatief_9,
    "Immigratie_10" AS immigratie_10,
    "UitAndereGemeente_11" AS uitanderegemeente_11,
    "TotaalVertrekInclusiefCorrecties_12" AS totaalvertrekinclusiefcorrecties_12,
    "TotaalVertrekInclusiefCoRelatief_13" AS totaalvertrekinclusiefcorelatief_13,
    "EmigratieInclusiefAdministratieveC_14" AS emigratieinclusiefadministratievec_14,
    "SaldoAdministratieveCorrecties_15" AS saldoadministratievecorrecties_15,
    "NaarAndereGemeente_16" AS naaranderegemeente_16,
    "VestigingsoverschotInclusiefCorrecties_17" AS vestigingsoverschotinclusiefcorrecties_17,
    "TotaleGroei_18" AS totalegroei_18,
    "TotaleGroeiRelatief_19" AS totalegroeirelatief_19,
    "BevolkingOp31December_20" AS bevolkingop31december_20,
    "Geslacht_label" AS geslacht_label,
    "RegioS_label" AS regios_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-37259ned"
