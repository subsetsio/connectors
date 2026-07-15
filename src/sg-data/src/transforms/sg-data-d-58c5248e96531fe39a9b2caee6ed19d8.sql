-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "English" AS english,
    "Mandarin" AS mandarin,
    "ChineseDialects" AS chinesedialects,
    "Malay" AS malay,
    "Tamil" AS tamil,
    "OtherIndianLanguages" AS otherindianlanguages,
    "Others" AS others
FROM "sg-data-d-58c5248e96531fe39a9b2caee6ed19d8"
