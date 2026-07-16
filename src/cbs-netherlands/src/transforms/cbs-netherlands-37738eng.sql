-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Vegetables" AS vegetables,
    "Periodes" AS periodes,
    "GrossYield_1" AS grossyield_1,
    "CroppingArea_2" AS croppingarea_2,
    "Vegetables_label" AS vegetables_label,
    "Periodes_label" AS periodes_label
FROM "cbs-netherlands-37738eng"
