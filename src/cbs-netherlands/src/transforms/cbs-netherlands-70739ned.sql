-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "RegioS" AS regios,
    "Begindatum_1" AS begindatum_1,
    "Einddatum_2" AS einddatum_2,
    "GebiedsOfGemeentecode_3" AS gebiedsofgemeentecode_3,
    "Provincie_4" AS provincie_4,
    "ProvincieAfkorting_5" AS provincieafkorting_5,
    "BegindatumSorteerveld_6" AS begindatumsorteerveld_6,
    "EinddatumSorteerveld_7" AS einddatumsorteerveld_7,
    "RegioS_label" AS regios_label
FROM "cbs-netherlands-70739ned"
