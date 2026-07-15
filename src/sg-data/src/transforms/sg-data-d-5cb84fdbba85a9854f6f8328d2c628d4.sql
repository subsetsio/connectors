-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "applicationNumber" AS applicationnumber,
    "filingDate" AS filingdate,
    "classSubClass" AS classsubclass,
    "status",
    "approvedDate" AS approveddate,
    "ukDesignNum" AS ukdesignnum,
    "ukRegistrationDate" AS ukregistrationdate,
    "internationalRegistrationNum" AS internationalregistrationnum,
    "internationalRegistrationDate" AS internationalregistrationdate,
    "renewalDueDate" AS renewalduedate,
    "expiryDate" AS expirydate,
    "lodgementDate" AS lodgementdate,
    "lastModifiedDate" AS lastmodifieddate,
    "articleDetails_json" AS articledetails_json,
    "applicantDetails_json" AS applicantdetails_json,
    "applicantTypeDetails_json" AS applicanttypedetails_json,
    "priorityDetails_json" AS prioritydetails_json,
    "agentDetails_json" AS agentdetails_json,
    "journalDetails_json" AS journaldetails_json,
    "licenseInfo_json" AS licenseinfo_json,
    "otherEntries_json" AS otherentries_json,
    "documents_json"
FROM "sg-data-d-5cb84fdbba85a9854f6f8328d2c628d4"
