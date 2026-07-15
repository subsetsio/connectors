-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "NotLiterate" AS notliterate,
    "Literate" AS literate,
    "OneLanguageOnly_ChineseOnly" AS onelanguageonly_chineseonly,
    "OneLanguageOnly_EnglishOnly" AS onelanguageonly_englishonly,
    "OneLanguageOnly_MalayOnly" AS onelanguageonly_malayonly,
    "OneLanguageOnly_TamilOnly" AS onelanguageonly_tamilonly,
    "OneLanguageOnly_Non_OfficialLanguageOnly" AS onelanguageonly_non_officiallanguageonly,
    "TwoLanguagesOnly_EnglishandChineseOnly" AS twolanguagesonly_englishandchineseonly,
    "TwoLanguagesOnly_EnglishandMalayOnly" AS twolanguagesonly_englishandmalayonly,
    "TwoLanguagesOnly_EnglishandTamilOnly" AS twolanguagesonly_englishandtamilonly,
    "TwoLanguagesOnly_EnglishandNon_OfficialLanguageOnly" AS twolanguagesonly_englishandnon_officiallanguageonly,
    "TwoLanguagesOnly_OtherTwoLanguagesOnly" AS twolanguagesonly_othertwolanguagesonly,
    "ThreeOrMoreLanguages_English_ChineseandMalayOnly" AS threeormorelanguages_english_chineseandmalayonly,
    "ThreeOrMoreLanguages_English_MalayandTamilOnly" AS threeormorelanguages_english_malayandtamilonly,
    "ThreeOrMoreLanguages_OtherThreeOrMoreLanguages" AS threeormorelanguages_otherthreeormorelanguages
FROM "sg-data-d-48f5108ddcd0989601283c33f44b7673"
