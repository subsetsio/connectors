-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is specific to South Africa land-consumption measures; do not combine it with global street-density tables without harmonizing geography and metric definitions.
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
