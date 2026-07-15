-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Chinese_English" AS chinese_english,
    "Chinese_Mandarin" AS chinese_mandarin,
    "Chinese_ChineseDialects" AS chinese_chinesedialects,
    "Chinese_Others" AS chinese_others,
    "Malays_English" AS malays_english,
    "Malays_Malay" AS malays_malay,
    "Malays_Others" AS malays_others,
    "Indians_English" AS indians_english,
    "Indians_Malay" AS indians_malay,
    "Indians_Tamil" AS indians_tamil,
    "Indians_OtherIndianLanguages" AS indians_otherindianlanguages,
    "Indians_Others" AS indians_others,
    "Others_English" AS others_english,
    "Others_Malay" AS others_malay,
    "Others_Others" AS others_others
FROM "sg-data-d-6f7172f5e7f4a522c9de987293b7ecd4"
