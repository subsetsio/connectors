-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "HouseholdswithAllMembersWithoutALotofDifficultyinPerformingAnyB" AS householdswithallmemberswithoutalotofdifficultyinperforminganyb,
    "HouseholdswithAtLeastOneMemberUnabletoPerform_withALotofDifficu" AS householdswithatleastonememberunabletoperform_withalotofdifficu
FROM "sg-data-d-0145fb635a7112d530c4edb0e814b8a9"
