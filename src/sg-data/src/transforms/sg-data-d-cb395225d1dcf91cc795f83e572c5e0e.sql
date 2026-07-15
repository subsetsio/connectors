-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "applicationNumber" AS applicationnumber,
    "applicationStatus" AS applicationstatus,
    "applicationType" AS applicationtype,
    "filingDate" AS filingdate,
    "lodgementDate" AS lodgementdate,
    "titleOfInvention" AS titleofinvention,
    "ipc",
    "dateOfPublication" AS dateofpublication,
    "publicationPatentNumForOldApplication" AS publicationpatentnumforoldapplication,
    "lastModifiedDate" AS lastmodifieddate,
    "inventors_json",
    "applicants_json",
    "currentApplicants_json" AS currentapplicants_json,
    "agents_json",
    "priorities_json",
    "registerDetails_json" AS registerdetails_json,
    "pctPriorityClaimed_json" AS pctpriorityclaimed_json,
    "pctApplications_json" AS pctapplications_json,
    "hmgStatus_json" AS hmgstatus_json,
    "licenses_json",
    "grantorParticulars_json" AS grantorparticulars_json,
    "granteeParticulars_json" AS granteeparticulars_json,
    "securityInterests_json" AS securityinterests_json,
    "transferOfOwnerships_json" AS transferofownerships_json,
    "rupka_json",
    "documents_json",
    "otherEntries_json" AS otherentries_json,
    "divisionalApplications_json" AS divisionalapplications_json
FROM "sg-data-d-cb395225d1dcf91cc795f83e572c5e0e"
