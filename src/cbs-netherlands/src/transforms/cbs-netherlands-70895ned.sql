-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geslacht" AS geslacht,
    "LeeftijdOp31December" AS leeftijdop31december,
    "Perioden" AS perioden,
    "Overledenen_1" AS overledenen_1,
    "Geslacht_label" AS geslacht_label,
    "LeeftijdOp31December_label" AS leeftijdop31december_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-70895ned"
