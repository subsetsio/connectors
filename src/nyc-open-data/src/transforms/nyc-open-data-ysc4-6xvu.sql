-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "by_nta",
    "households_with_0_isp",
    "households_with_1_isp",
    "households_with_2_isp",
    "households_with_34_isp",
    "households_with_5_isp"
FROM "nyc-open-data-ysc4-6xvu"
