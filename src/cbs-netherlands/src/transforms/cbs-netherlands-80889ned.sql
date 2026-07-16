-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "RegioS" AS regios,
    "Perioden" AS perioden,
    "TariefOpcentenMotorrijtuigenbelasting_1" AS tariefopcentenmotorrijtuigenbelasting_1,
    "RegioS_label" AS regios_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80889ned"
