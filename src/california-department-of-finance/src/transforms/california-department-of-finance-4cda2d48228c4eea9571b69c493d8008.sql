-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Block-to-place crosswalk includes both block and E-5 place codes; use the full grain when joining to avoid duplicating block populations across places.
SELECT
    "OBJECTID" AS objectid,
    "B_GEOID" AS b_geoid,
    "COUNTY" AS county,
    "E5_PLACE" AS e5_place,
    "E5_PLACE25" AS e5_place25,
    "HU_TU_20" AS hu_tu_20,
    "HU_TU_25" AS hu_tu_25,
    "Change_N" AS change_n,
    "Change_P" AS change_p,
    "C_Block" AS c_block,
    CAST("C_BlockGro" AS BIGINT) AS c_blockgro,
    "C_Tract" AS c_tract,
    "COUNTY_N" AS county_n,
    "E5PLACE25" AS e5place25
FROM "california-department-of-finance-4cda2d48228c4eea9571b69c493d8008"
