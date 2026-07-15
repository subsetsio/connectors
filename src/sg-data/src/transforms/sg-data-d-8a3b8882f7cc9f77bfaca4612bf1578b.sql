-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "English" AS english,
    "Mandarin" AS mandarin,
    "ChineseDialects_Total" AS chinesedialects_total,
    "ChineseDialects_Hokkien" AS chinesedialects_hokkien,
    "ChineseDialects_Teochew" AS chinesedialects_teochew,
    "ChineseDialects_Cantonese" AS chinesedialects_cantonese,
    "ChineseDialects_OtherChineseDialects" AS chinesedialects_otherchinesedialects,
    "Malay" AS malay,
    "IndianLanguages_Total" AS indianlanguages_total,
    "IndianLanguages_Tamil" AS indianlanguages_tamil,
    "IndianLanguages_OtherIndianLanguages" AS indianlanguages_otherindianlanguages,
    "Others" AS others
FROM "sg-data-d-8a3b8882f7cc9f77bfaca4612bf1578b"
