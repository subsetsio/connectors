-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "ReligionOfHusband_NoReligion" AS religionofhusband_noreligion,
    "ReligionOfHusband_Buddhism" AS religionofhusband_buddhism,
    "ReligionOfHusband_Taoism1" AS religionofhusband_taoism1,
    "ReligionOfHusband_Islam" AS religionofhusband_islam,
    "ReligionOfHusband_Hinduism" AS religionofhusband_hinduism,
    "ReligionOfHusband_Sikhism" AS religionofhusband_sikhism,
    "ReligionOfHusband_Christianity_Catholic" AS religionofhusband_christianity_catholic,
    "ReligionOfHusband_Christianity_OtherChristians" AS religionofhusband_christianity_otherchristians,
    "ReligionOfHusband_OtherReligions" AS religionofhusband_otherreligions
FROM "sg-data-d-2d492ad4b5c76c6bfa4ca5a3a7f3fa60"
