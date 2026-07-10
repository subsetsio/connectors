-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are geographic disaster summaries, not household-level owner records; avoid summing across overlapping place levels without filtering the geography fields.
SELECT
    "id",
    "disasterNumber" AS disasternumber,
    "state",
    "county",
    "city",
    "zipCode" AS zipcode,
    "validRegistrations" AS validregistrations,
    "averageFemaInspectedDamage" AS averagefemainspecteddamage,
    "totalInspected" AS totalinspected,
    "totalDamage" AS totaldamage,
    "noFemaInspectedDamage" AS nofemainspecteddamage,
    "femaInspectedDamageBetween1And10000" AS femainspecteddamagebetween1and10000,
    "femaInspectedDamageBetween10001And20000" AS femainspecteddamagebetween10001and20000,
    "femaInspectedDamageBetween20001And30000" AS femainspecteddamagebetween20001and30000,
    "femaInspectedDamageGreaterThan30000" AS femainspecteddamagegreaterthan30000,
    "approvedForFemaAssistance" AS approvedforfemaassistance,
    "totalApprovedIhpAmount" AS totalapprovedihpamount,
    "repairReplaceAmount" AS repairreplaceamount,
    "rentalAmount" AS rentalamount,
    "otherNeedsAmount" AS otherneedsamount,
    "approvedBetween1And10000" AS approvedbetween1and10000,
    "approvedBetween10001And25000" AS approvedbetween10001and25000,
    "approvedBetween25001AndMax" AS approvedbetween25001andmax,
    "totalMaxGrants" AS totalmaxgrants
FROM "fema-housingassistanceowners"
