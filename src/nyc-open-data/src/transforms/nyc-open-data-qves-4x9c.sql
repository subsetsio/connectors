-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "permitno",
    "expiration_date",
    "effectivedate",
    "companyname",
    "companycity",
    "companystate",
    "companyzip",
    "issuedate",
    "validdates",
    "validtimes",
    "schoolchildren",
    "othertransportdesc",
    "permitpurpose",
    "pelham",
    "beltparkway",
    "bronxriver",
    "crossisland",
    "easternparkway",
    "grandcentral",
    "mosholu",
    "hutchinsonriver",
    "harlemriver",
    "richmondparkway",
    "willowbrookparkway",
    "henryhudsonparkway",
    "jackierobinsonparkway",
    "fdr_drive",
    "otherparkway",
    "otherparkwaydesc",
    "conditionrestrictions"
FROM "nyc-open-data-qves-4x9c"
