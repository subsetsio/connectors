-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Citizenship" AS citizenship,
    "Periods" AS periods,
    "TotalRequestsAsylumAndFamilyMembers_1" AS totalrequestsasylumandfamilymembers_1,
    "FirstRequestsForAsylumPersons_2" AS firstrequestsforasylumpersons_2,
    "SubsequentRequests_3" AS subsequentrequests_3,
    "FamilyMembersPersons_4" AS familymemberspersons_4,
    "Citizenship_label" AS citizenship_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-80059eng"
