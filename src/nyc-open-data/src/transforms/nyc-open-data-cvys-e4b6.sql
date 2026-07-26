-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "permitno",
    "effectivedate",
    "expirationdate",
    "companyid",
    "companyname",
    "issuedate",
    "validdays",
    "validtimes",
    "fleet_1",
    "permitoption",
    "validfor",
    "buscompany",
    "permitpurpose",
    "policeescort",
    "dotescort",
    "otherescort",
    "otherescortdesc",
    "conditionrestrictions",
    "permitrevoked",
    "reasonrevoked",
    "daterevoked"
FROM "nyc-open-data-cvys-e4b6"
