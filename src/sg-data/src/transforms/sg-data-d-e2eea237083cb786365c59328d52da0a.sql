-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "HouseholdswithAllMembersWithoutALotofDifficultyinPerformingAnyB" AS householdswithallmemberswithoutalotofdifficultyinperforminganyb,
    "HouseholdswithAtLeastOneMemberUnabletoPerform_withALotofDifficu" AS householdswithatleastonememberunabletoperform_withalotofdifficu
FROM "sg-data-d-e2eea237083cb786365c59328d52da0a"
