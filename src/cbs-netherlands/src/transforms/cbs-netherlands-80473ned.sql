-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SBI2008" AS sbi2008,
    "Perioden" AS perioden,
    "OpenstaandeVacatures_1" AS openstaandevacatures_1,
    "OntstaneVacatures_2" AS ontstanevacatures_2,
    "VervuldeVacatures_3" AS vervuldevacatures_3,
    "SBI2008_label" AS sbi2008_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80473ned"
