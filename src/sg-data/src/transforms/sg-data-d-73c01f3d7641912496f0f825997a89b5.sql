-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Chinese_English" AS chinese_english,
    "Chinese_Mandarin" AS chinese_mandarin,
    "Chinese_ChineseDialects" AS chinese_chinesedialects,
    "Chinese_Others1" AS chinese_others1,
    "Malays_English" AS malays_english,
    "Malays_Malay" AS malays_malay,
    "Malays_Others1" AS malays_others1,
    "Indians_English" AS indians_english,
    "Indians_Malay" AS indians_malay,
    "Indians_Tamil" AS indians_tamil,
    "Indians_OtherIndianLanguages" AS indians_otherindianlanguages,
    "Indians_Others1" AS indians_others1,
    "Others_English" AS others_english,
    "Others_Malay" AS others_malay,
    "Others_Others1" AS others_others1
FROM "sg-data-d-73c01f3d7641912496f0f825997a89b5"
