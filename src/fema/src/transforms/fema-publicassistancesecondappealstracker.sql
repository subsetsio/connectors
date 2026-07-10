-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "region",
    "disasterNumber" AS disasternumber,
    "declarationType" AS declarationtype,
    "recipient",
    "appellant",
    "applicantId" AS applicantid,
    "pwgmpNumber" AS pwgmpnumber,
    "status",
    "hqReceivedDate" AS hqreceiveddate,
    "emailAcknowledgementDate" AS emailacknowledgementdate,
    "rfiSentDate" AS rfisentdate,
    "rfiDueDate" AS rfiduedate,
    "rfiReceivedDate" AS rfireceiveddate,
    "decisionSignedDate" AS decisionsigneddate,
    "id"
FROM "fema-publicassistancesecondappealstracker"
