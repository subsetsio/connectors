-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "NoReligion" AS noreligion,
    "Buddhism" AS buddhism,
    "Taoism1" AS taoism1,
    "Islam" AS islam,
    "Hinduism" AS hinduism,
    "Sikhism" AS sikhism,
    "Christianity_Catholic" AS christianity_catholic,
    "Christianity_OtherChristians" AS christianity_otherchristians,
    "OtherReligions" AS otherreligions
FROM "sg-data-d-a58564fbed922609a0f79af96069dd9b"
