-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "LeeftijdKindEren" AS leeftijdkinderen,
    "RegioS" AS regios,
    "Perioden" AS perioden,
    "TotaalHuishoudensMetKinderen_1" AS totaalhuishoudensmetkinderen_1,
    "k_1Kind_2" AS k_1kind_2,
    "k_2Kinderen_3" AS k_2kinderen_3,
    "k_3OfMeerKinderen_4" AS k_3ofmeerkinderen_4,
    "TotaalNietGehuwdeParenMetKinderen_5" AS totaalnietgehuwdeparenmetkinderen_5,
    "k_1Kind_6" AS k_1kind_6,
    "k_2Kinderen_7" AS k_2kinderen_7,
    "k_3OfMeerKinderen_8" AS k_3ofmeerkinderen_8,
    "TotaalGehuwdeParenMetKinderen_9" AS totaalgehuwdeparenmetkinderen_9,
    "k_1Kind_10" AS k_1kind_10,
    "k_2Kinderen_11" AS k_2kinderen_11,
    "k_3OfMeerKinderen_12" AS k_3ofmeerkinderen_12,
    "TotaalEenouderhuishoudensMetKinderen_13" AS totaaleenouderhuishoudensmetkinderen_13,
    "k_1Kind_14" AS k_1kind_14,
    "k_2Kinderen_15" AS k_2kinderen_15,
    "k_3OfMeerKinderen_16" AS k_3ofmeerkinderen_16,
    "LeeftijdKindEren_label" AS leeftijdkinderen_label,
    "RegioS_label" AS regios_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-71487ned"
