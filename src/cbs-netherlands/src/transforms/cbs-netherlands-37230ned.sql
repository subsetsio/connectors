-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "RegioS" AS regios,
    "Perioden" AS perioden,
    "BevolkingAanHetBeginVanDePeriode_1" AS bevolkingaanhetbeginvandeperiode_1,
    "LevendGeborenKinderen_2" AS levendgeborenkinderen_2,
    "Overledenen_3" AS overledenen_3,
    "TotaleVestiging_4" AS totalevestiging_4,
    "VestigingVanuitEenAndereGemeente_5" AS vestigingvanuiteenanderegemeente_5,
    "Immigratie_6" AS immigratie_6,
    "TotaalVertrekInclAdmCorrecties_7" AS totaalvertrekincladmcorrecties_7,
    "VertrekNaarAndereGemeente_8" AS vertreknaaranderegemeente_8,
    "EmigratieInclusiefAdmCorrecties_9" AS emigratieinclusiefadmcorrecties_9,
    "OverigeCorrecties_10" AS overigecorrecties_10,
    "Bevolkingsgroei_11" AS bevolkingsgroei_11,
    "BevolkingsgroeiRelatief_12" AS bevolkingsgroeirelatief_12,
    "BevolkingsgroeiSinds1Januari_13" AS bevolkingsgroeisinds1januari_13,
    "BevolkingsgroeiSinds1JanuariRela_14" AS bevolkingsgroeisinds1januarirela_14,
    "BevolkingAanHetEindeVanDePeriode_15" AS bevolkingaanheteindevandeperiode_15,
    "RegioS_label" AS regios_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-37230ned"
