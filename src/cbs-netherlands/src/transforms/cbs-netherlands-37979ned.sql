-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geslacht" AS geslacht,
    "Perioden" AS perioden,
    "Overledenen_1" AS overledenen_1,
    "OverledenenRelatief_2" AS overledenenrelatief_2,
    "OverledenenGestandaardiseerd_3" AS overledenengestandaardiseerd_3,
    "Zuigelingensterfte_4" AS zuigelingensterfte_4,
    "ZuigelingensterfteRelatief_5" AS zuigelingensterfterelatief_5,
    "OverledenenJongerDan4Weken_6" AS overledenenjongerdan4weken_6,
    "OverledenenJongerDan4WekenRelatief_7" AS overledenenjongerdan4wekenrelatief_7,
    "PerinataleSterfte24_8" AS perinatalesterfte24_8,
    "PerinataleSterfte24Relatief_9" AS perinatalesterfte24relatief_9,
    "PerinataleSterfte28_10" AS perinatalesterfte28_10,
    "PerinataleSterfte28Relatief_11" AS perinatalesterfte28relatief_11,
    "LevensverwachtingBijGeboorte_12" AS levensverwachtingbijgeboorte_12,
    "GemiddeldeLeeftijdBijOverlijden_13" AS gemiddeldeleeftijdbijoverlijden_13,
    "Geslacht_label" AS geslacht_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-37979ned"
