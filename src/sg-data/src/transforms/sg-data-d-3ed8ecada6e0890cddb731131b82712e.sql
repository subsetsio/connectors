-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Chinese_English" AS chinese_english,
    "Chinese_Mandarin" AS chinese_mandarin,
    "Chinese_ChineseDialects" AS chinese_chinesedialects,
    "Chinese_Others3" AS chinese_others3,
    "Malays_English" AS malays_english,
    "Malays_Malay" AS malays_malay,
    "Malays_Others3" AS malays_others3,
    "Indians_English" AS indians_english,
    "Indians_Malay" AS indians_malay,
    "Indians_Tamil" AS indians_tamil,
    "Indians_OtherIndianLanguages" AS indians_otherindianlanguages,
    "Indians_Others3" AS indians_others3,
    "Others_English" AS others_english,
    "Others_Malay" AS others_malay,
    "Others_Others3" AS others_others3
FROM "sg-data-d-3ed8ecada6e0890cddb731131b82712e"
