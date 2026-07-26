-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_month" AS month,
    "borough",
    "communitydistrict",
    "refusetonscollected",
    "papertonscollected",
    "mgptonscollected",
    "resorganicstons",
    "schoolorganictons",
    "leavesorganictons",
    "xmastreetons",
    "otherorganicstons",
    "borough_id"
FROM "nyc-open-data-ebb7-mvp5"
