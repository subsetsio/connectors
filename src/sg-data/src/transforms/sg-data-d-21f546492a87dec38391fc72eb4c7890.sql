-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total" AS total,
    "English_Total" AS english_total,
    "English_EnglishOnly" AS english_englishonly,
    "English_EnglishandMandarin" AS english_englishandmandarin,
    "English_EnglishandChineseDialect" AS english_englishandchinesedialect,
    "English_EnglishandMalay" AS english_englishandmalay,
    "English_EnglishandTamil" AS english_englishandtamil,
    "English_EnglishandOtherIndianLanguage" AS english_englishandotherindianlanguage,
    "English_EnglishandOtherLanguage" AS english_englishandotherlanguage,
    "Mandarin_Total1" AS mandarin_total1,
    "Mandarin_MandarinOnly" AS mandarin_mandarinonly,
    "Mandarin_MandarinandEnglish" AS mandarin_mandarinandenglish,
    "Mandarin_MandarinandChineseDialect" AS mandarin_mandarinandchinesedialect,
    "ChineseDialects_Total1" AS chinesedialects_total1,
    "ChineseDialects_ChineseDialectOnly" AS chinesedialects_chinesedialectonly,
    "ChineseDialects_ChineseDialectandEnglish" AS chinesedialects_chinesedialectandenglish,
    "ChineseDialects_ChineseDialectandMandarin" AS chinesedialects_chinesedialectandmandarin,
    "Malay_Total1" AS malay_total1,
    "Malay_MalayOnly" AS malay_malayonly,
    "Malay_MalayandEnglish" AS malay_malayandenglish,
    "IndianLanguages_Total" AS indianlanguages_total,
    "IndianLanguages_Tamil_Total1" AS indianlanguages_tamil_total1,
    "IndianLanguages_Tamil_TamilOnly" AS indianlanguages_tamil_tamilonly,
    "IndianLanguages_Tamil_TamilandEnglish" AS indianlanguages_tamil_tamilandenglish,
    "IndianLanguages_OtherIndianLanguages_Total1" AS indianlanguages_otherindianlanguages_total1,
    "IndianLanguages_OtherIndianLanguages_OtherIndianLanguageandEngl" AS indianlanguages_otherindianlanguages_otherindianlanguageandengl,
    "OtherLanguages_Total1" AS otherlanguages_total1,
    "OtherLanguages_OtherLanguageandEnglish" AS otherlanguages_otherlanguageandenglish
FROM "sg-data-d-21f546492a87dec38391fc72eb4c7890"
