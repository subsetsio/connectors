-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Periods" AS periods,
    "PriceIndices_1" AS priceindices_1,
    "ChangesComparedToOneYearEarlier_2" AS changescomparedtooneyearearlier_2,
    "PriceIndices_3" AS priceindices_3,
    "ChangesComparedToOneYearEarlier_4" AS changescomparedtooneyearearlier_4,
    "PriceIndices_5" AS priceindices_5,
    "ChangesComparedToOneYearEarlier_6" AS changescomparedtooneyearearlier_6,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-80444eng"
