-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
SELECT
    "__sheet__" AS sheet,
    "Year" AS year,
    "Bricklayers" AS bricklayers,
    "Carpenters" AS carpenters,
    "Masons" AS masons,
    "Plumbers" AS plumbers,
    "shilling, UK market price" AS shilling_uk_market_price,
    "Bricklayers_2" AS bricklayers_2,
    "Carpenters_2" AS carpenters_2,
    "Masons_2" AS masons_2,
    "Plumbers_2" AS plumbers_2,
    "pence per kg" AS pence_per_kg,
    "shillings per kg" AS shillings_per_kg,
    "pence per kg_2" AS pence_per_kg_2,
    "shilling per liter" AS shilling_per_liter,
    "shilling per liter_2" AS shilling_per_liter_2,
    "shilling per liter_3" AS shilling_per_liter_3,
    "shilling per liter_4" AS shilling_per_liter_4,
    "shilling per liter_5" AS shilling_per_liter_5,
    "shilling per ton" AS shilling_per_ton,
    "shilling per ton_2" AS shilling_per_ton_2,
    "shilling per ton_3" AS shilling_per_ton_3,
    "per gram Ag" AS per_gram_ag,
    "per gram Ag_2" AS per_gram_ag_2,
    "mint",
    "market",
    "per kg" AS per_kg,
    "per kg_2" AS per_kg_2,
    "per liter" AS per_liter,
    "per liter_2" AS per_liter_2,
    "per liter_3" AS per_liter_3,
    "per liter_4" AS per_liter_4,
    "per liter_5" AS per_liter_5,
    "per ton" AS per_ton,
    "per ton_2" AS per_ton_2,
    "per ton_3" AS per_ton_3
FROM "gpih-van-diemen-land-1806-50"
