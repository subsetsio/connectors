-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "arid",
    "agencyname",
    "agencydesc",
    "parkingplacardnumber",
    "parkingplacardtype",
    "issuingauthority",
    "governmentvehicle",
    "privatevehicle",
    "vehicleplatestate",
    "agencytype",
    "applicationplacardtype",
    "parkingrestriction",
    "active",
    "activepermit",
    "abpermitnumber",
    "abp_issuedate",
    "abp_effectivedate",
    "abp_expirationdate",
    "issuereason",
    "abpermitrecordsactive",
    "permittype",
    "deactivatedate",
    "returned",
    "returndate"
FROM "nyc-open-data-a23q-dmjn"
