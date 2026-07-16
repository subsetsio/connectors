-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "BedrijfskenmerkenSBI2008" AS bedrijfskenmerkensbi2008,
    "Perioden" AS perioden,
    "Ziekteverzuimpercentage_1" AS ziekteverzuimpercentage_1,
    "BedrijfskenmerkenSBI2008_label" AS bedrijfskenmerkensbi2008_label,
    "Perioden_label" AS perioden_label
FROM "cbs-netherlands-80072ned"
