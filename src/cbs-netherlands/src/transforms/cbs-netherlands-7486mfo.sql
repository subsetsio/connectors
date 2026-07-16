-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ProvincialeHeffingen" AS provincialeheffingen,
    "RegioS" AS regios,
    "Perioden" AS perioden,
    "ProvincialeHeffingenInMlnEuro_1" AS provincialeheffingeninmlneuro_1,
    "ProvincialeHeffingen_label" AS provincialeheffingen_label,
    "RegioS_label" AS regios_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-7486mfo"
