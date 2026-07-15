-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "NoReligion" AS noreligion,
    "Buddhism" AS buddhism,
    "Taoism" AS taoism,
    "Islam" AS islam,
    "Hinduism" AS hinduism,
    "Sikhism" AS sikhism,
    "Christianity_Catholic" AS christianity_catholic,
    "Christianity_OtherChristians" AS christianity_otherchristians,
    "OtherReligions" AS otherreligions
FROM "sg-data-d-d4be7f8ba23ba93e5d59564d1dfb5eaa"
