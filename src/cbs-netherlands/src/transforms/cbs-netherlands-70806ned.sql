-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "RegioS" AS regios,
    "SoortRijbanen" AS soortrijbanen,
    "Perioden" AS perioden,
    "Weglengte_1" AS weglengte_1,
    "RegioS_label" AS regios_label,
    "SoortRijbanen_label" AS soortrijbanen_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-70806ned"
