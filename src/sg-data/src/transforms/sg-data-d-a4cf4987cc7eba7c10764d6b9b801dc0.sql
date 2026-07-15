-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "NotLiterate" AS notliterate,
    "Literate" AS literate,
    "OneLanguageOnly_EnglishOnly" AS onelanguageonly_englishonly,
    "OneLanguageOnly_ChineseOnly" AS onelanguageonly_chineseonly,
    "OneLanguageOnly_MalayOnly" AS onelanguageonly_malayonly,
    "OneLanguageOnly_TamilOnly" AS onelanguageonly_tamilonly,
    "OneLanguageOnly_Non_OfficialLanguageOnly" AS onelanguageonly_non_officiallanguageonly,
    "TwoLanguagesOnly_EnglishandChineseOnly" AS twolanguagesonly_englishandchineseonly,
    "TwoLanguagesOnly_EnglishandMalayOnly" AS twolanguagesonly_englishandmalayonly,
    "TwoLanguagesOnly_EnglishandTamilOnly" AS twolanguagesonly_englishandtamilonly,
    "TwoLanguagesOnly_EnglishandNon_OfficialLanguageOnly" AS twolanguagesonly_englishandnon_officiallanguageonly,
    "TwoLanguagesOnly_OtherTwoLanguagesOnly" AS twolanguagesonly_othertwolanguagesonly,
    "ThreeOrMoreLanguages" AS threeormorelanguages
FROM "sg-data-d-a4cf4987cc7eba7c10764d6b9b801dc0"
