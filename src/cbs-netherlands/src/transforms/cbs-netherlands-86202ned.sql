-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "InkomensgrensHuishouden" AS inkomensgrenshuishouden,
    "DuurInkomenspositie" AS duurinkomenspositie,
    "KenmerkenVanHuishoudens" AS kenmerkenvanhuishoudens,
    "RegioS" AS regios,
    "Perioden" AS perioden,
    "ParticuliereHuishoudens_1" AS particulierehuishoudens_1,
    "Personen_2" AS personen_2,
    "MinderjarigeKinderen_3" AS minderjarigekinderen_3,
    "ParticuliereHuishoudensRelatief_4" AS particulierehuishoudensrelatief_4,
    "PersonenRelatief_5" AS personenrelatief_5,
    "MinderjarigeKinderenRelatief_6" AS minderjarigekinderenrelatief_6,
    "InkomensgrensHuishouden_label" AS inkomensgrenshuishouden_label,
    "DuurInkomenspositie_label" AS duurinkomenspositie_label,
    "KenmerkenVanHuishoudens_label" AS kenmerkenvanhuishoudens_label,
    "RegioS_label" AS regios_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-86202ned"
