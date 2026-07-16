-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "GeslachtWerknemer" AS geslachtwerknemer,
    "Dienstverband" AS dienstverband,
    "Bedrijfsgrootte" AS bedrijfsgrootte,
    "BedrijfstakkenBranchesSBI2008" AS bedrijfstakkenbranchessbi2008,
    "Perioden" AS perioden,
    "Banen_1" AS banen_1,
    "Arbeidsvolume_2" AS arbeidsvolume_2,
    "Uurloon_3" AS uurloon_3,
    "MaandloonInclusiefOverwerk_4" AS maandlooninclusiefoverwerk_4,
    "MaandloonExclusiefOverwerk_5" AS maandloonexclusiefoverwerk_5,
    "JaarloonInclusiefBijzondereBeloning_6" AS jaarlooninclusiefbijzonderebeloning_6,
    "JaarloonExclusiefBijzondereBeloning_7" AS jaarloonexclusiefbijzonderebeloning_7,
    "BijzondereBeloning_8" AS bijzonderebeloning_8,
    "BijtellingAutoVanDeZaak_9" AS bijtellingautovandezaak_9,
    "PerBaanPerWeekInclusiefOverwerk_10" AS perbaanperweekinclusiefoverwerk_10,
    "PerBaanPerWeekExclusiefOverwerk_11" AS perbaanperweekexclusiefoverwerk_11,
    "PerBaanPerJaar_12" AS perbaanperjaar_12,
    "PerArbeidsjaar_13" AS perarbeidsjaar_13,
    "GeslachtWerknemer_label" AS geslachtwerknemer_label,
    "Dienstverband_label" AS dienstverband_label,
    "Bedrijfsgrootte_label" AS bedrijfsgrootte_label,
    "BedrijfstakkenBranchesSBI2008_label" AS bedrijfstakkenbranchessbi2008_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-81432ned"
