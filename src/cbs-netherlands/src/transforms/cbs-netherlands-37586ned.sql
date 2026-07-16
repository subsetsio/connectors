-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geslacht" AS geslacht,
    "LeeftijdOp31December" AS leeftijdop31december,
    "Perioden" AS perioden,
    "HuwendePersonen_1" AS huwendepersonen_1,
    "HuwendePersonenPer1000Inwoners_2" AS huwendepersonenper1000inwoners_2,
    "HuwendePersonenPer1000NietGehuwden_3" AS huwendepersonenper1000nietgehuwden_3,
    "VoorDeEersteMaalHuwendePersonen_4" AS voordeeerstemaalhuwendepersonen_4,
    "VoorDeEersteMaalHuwendenRelatief_5" AS voordeeerstemaalhuwendenrelatief_5,
    "HuwendenNaEerderPartnerschap_6" AS huwendennaeerderpartnerschap_6,
    "HuwendenNaPartnerschapRelatief_7" AS huwendennapartnerschaprelatief_7,
    "HertrouwendePersonen_8" AS hertrouwendepersonen_8,
    "HertrouwendePersonenRelatief_9" AS hertrouwendepersonenrelatief_9,
    "HertrouwendePersonenEerderVerweduwd_10" AS hertrouwendepersoneneerderverweduwd_10,
    "HertrouwendePersonenEerderGescheiden_11" AS hertrouwendepersoneneerdergescheiden_11,
    "Geslacht_label" AS geslacht_label,
    "LeeftijdOp31December_label" AS leeftijdop31december_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-37586ned"
