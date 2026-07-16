-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "RegioS" AS regios,
    "Perioden" AS perioden,
    "TotaleOppervlakteGrasland_1" AS totaleoppervlaktegrasland_1,
    "TotaleGemaaideOppervlakteGrasland_2" AS totalegemaaideoppervlaktegrasland_2,
    "Kuilgras_3" AS kuilgras_3,
    "Hooi_4" AS hooi_4,
    "Zomerstalvoedering_5" AS zomerstalvoedering_5,
    "Overig_6" AS overig_6,
    "TotaleOogstKuilgras_7" AS totaleoogstkuilgras_7,
    "MetDrogeStofgehalte35Procent_8" AS metdrogestofgehalte35procent_8,
    "MetDrogeStofgehalte35Procent_9" AS metdrogestofgehalte35procent_9,
    "TotaleOogstHooi_10" AS totaleoogsthooi_10,
    "VoorraadKuilgras_11" AS voorraadkuilgras_11,
    "VoorraadHooi_12" AS voorraadhooi_12,
    "RegioS_label" AS regios_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-7140gras"
