-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SectorBranchesSIC2008" AS sectorbranchessic2008,
    "Margins" AS margins,
    "SeasonalAdjustment" AS seasonaladjustment,
    "Periods" AS periods,
    "ProducerConfidence_1" AS producerconfidence_1,
    "ExpectedActivity_2" AS expectedactivity_2,
    "OpinionOnOrderBooks_3" AS opiniononorderbooks_3,
    "StocksOfFinishedProducts_4" AS stocksoffinishedproducts_4,
    "SectorBranchesSIC2008_label" AS sectorbranchessic2008_label,
    "Margins_label" AS margins_label,
    "SeasonalAdjustment_label" AS seasonaladjustment_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-81234eng"
