-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "English" AS english,
    "Mandarin" AS mandarin,
    "ChineseDialects" AS chinesedialects,
    "Malay" AS malay,
    "Tamil" AS tamil,
    "OtherIndianLanguages" AS otherindianlanguages,
    "Others" AS others
FROM "sg-data-d-c4ed6ab54bc73259941436802e7b2e6f"
