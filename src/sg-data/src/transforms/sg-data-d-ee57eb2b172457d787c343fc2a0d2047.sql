-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "NoReligion" AS noreligion,
    "Buddhism" AS buddhism,
    "Taoism_ChineseTraditionalBeliefs" AS taoism_chinesetraditionalbeliefs,
    "Islam" AS islam,
    "Hinduism" AS hinduism,
    "Christianity_Catholic" AS christianity_catholic,
    "Christianity_OtherChristians" AS christianity_otherchristians,
    "OtherReligions" AS otherreligions
FROM "sg-data-d-ee57eb2b172457d787c343fc2a0d2047"
