-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "ReligionofHusband_NoReligion" AS religionofhusband_noreligion,
    "ReligionofHusband_Buddhism" AS religionofhusband_buddhism,
    "ReligionofHusband_Taoism1" AS religionofhusband_taoism1,
    "ReligionofHusband_Islam" AS religionofhusband_islam,
    "ReligionofHusband_Hinduism" AS religionofhusband_hinduism,
    "ReligionofHusband_Sikhism" AS religionofhusband_sikhism,
    "ReligionofHusband_Christianity_Catholic" AS religionofhusband_christianity_catholic,
    "ReligionofHusband_Christianity_OtherChristians" AS religionofhusband_christianity_otherchristians,
    "ReligionofHusband_OtherReligions" AS religionofhusband_otherreligions
FROM "sg-data-d-95b8089865ff5e690a684e7305ae90f7"
