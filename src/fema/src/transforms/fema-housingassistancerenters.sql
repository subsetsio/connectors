-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are geographic disaster summaries, not household-level renter records; avoid summing across overlapping place levels without filtering the geography fields.
SELECT
    "id",
    "disasterNumber" AS disasternumber,
    "state",
    "county",
    "city",
    "zipCode" AS zipcode,
    "validRegistrations" AS validregistrations,
    "totalInspected" AS totalinspected,
    "totalInspectedWithNoDamage" AS totalinspectedwithnodamage,
    "totalWithModerateDamage" AS totalwithmoderatedamage,
    "totalWithMajorDamage" AS totalwithmajordamage,
    "totalWithSubstantialDamage" AS totalwithsubstantialdamage,
    "approvedForFemaAssistance" AS approvedforfemaassistance,
    "totalApprovedIhpAmount" AS totalapprovedihpamount,
    "repairReplaceAmount" AS repairreplaceamount,
    "rentalAmount" AS rentalamount,
    "otherNeedsAmount" AS otherneedsamount,
    "approvedBetween1And10000" AS approvedbetween1and10000,
    "approvedBetween10001And25000" AS approvedbetween10001and25000,
    "approvedBetween25001AndMax" AS approvedbetween25001andmax,
    "totalMaxGrants" AS totalmaxgrants
FROM "fema-housingassistancerenters"
