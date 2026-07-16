-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PrognoseWaarneming" AS prognosewaarneming,
    "Perioden" AS perioden,
    "Bevolkingsomvang_1" AS bevolkingsomvang_1,
    "Bevolkingsgroei_2" AS bevolkingsgroei_2,
    "k_0Tot20Jaar_3" AS k_0tot20jaar_3,
    "k_20Tot65Jaar_4" AS k_20tot65jaar_4,
    "k_65JaarOfOuder_5" AS k_65jaarofouder_5,
    "k_0Tot20Jaar_6" AS k_0tot20jaar_6,
    "k_20Tot65Jaar_7" AS k_20tot65jaar_7,
    "k_65JaarOfOuder_8" AS k_65jaarofouder_8,
    "TotaleDruk_9" AS totaledruk_9,
    "GroeneDruk_10" AS groenedruk_10,
    "GrijzeDruk_11" AS grijzedruk_11,
    "LevendGeborenKinderen_12" AS levendgeborenkinderen_12,
    "TotaalVruchtbaarheidscijfer_13" AS totaalvruchtbaarheidscijfer_13,
    "Overledenen_14" AS overledenen_14,
    "Mannen_15" AS mannen_15,
    "Vrouwen_16" AS vrouwen_16,
    "Immigratie_17" AS immigratie_17,
    "EmigratieInclusiefCorrecties_18" AS emigratieinclusiefcorrecties_18,
    "MigratiesaldoInclusiefCorrecties_19" AS migratiesaldoinclusiefcorrecties_19,
    "PrognoseWaarneming_label" AS prognosewaarneming_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-70737ned"
