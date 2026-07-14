-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide table covering two fixed inter-census periods (1996-2001 and 2001-2011) plus built-up area per capita at three census years; the period is part of each column name rather than a value, and the two periods are different lengths so their rates are not directly comparable.
-- caution: South African cities only, despite the generic SDG 11.3.1 indicator name.
SELECT
    "source_item_id",
    "source_title",
    "source_type",
    "source_kind",
    "source_name",
    "source_row_number",
    "City" AS city,
    "Country" AS country,
    "Region" AS region,
    "LCR_1996_to_2001" AS lcr_1996_to_2001,
    "LCR_2001_to_2011" AS lcr_2001_to_2011,
    "PGR_1996_to_2001" AS pgr_1996_to_2001,
    "PGR_2001_to_2011" AS pgr_2001_to_2011,
    "LCRPGR_1996_to_2001" AS lcrpgr_1996_to_2001,
    "LCRPGR_2001_to_2011" AS lcrpgr_2001_to_2011,
    "BUP_area_per_Capita_1996" AS bup_area_per_capita_1996,
    "BUP_area_per_Capita_2001" AS bup_area_per_capita_2001,
    "BUP_area_per_Capita_2011" AS bup_area_per_capita_2011,
    "Estimate_source" AS estimate_source,
    "ObjectId" AS objectid
FROM "un-habitat-cc8c17fb67aa496e9feba634cec92446"
