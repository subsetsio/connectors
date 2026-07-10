-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "disasterNumber" AS disasternumber,
    "state",
    "county",
    "city",
    "zipCode" AS zipcode,
    "totalValidRegistrations" AS totalvalidregistrations,
    "validCallCenterRegistrations" AS validcallcenterregistrations,
    "validWebRegistrations" AS validwebregistrations,
    "validMobileRegistrations" AS validmobileregistrations,
    "ihpReferrals" AS ihpreferrals,
    "ihpEligible" AS ihpeligible,
    "ihpAmount" AS ihpamount,
    "haReferrals" AS hareferrals,
    "haEligible" AS haeligible,
    "haAmount" AS haamount,
    "onaReferrals" AS onareferrals,
    "onaEligible" AS onaeligible,
    "onaAmount" AS onaamount
FROM "fema-registrationintakeindividualshouseholdprograms"
