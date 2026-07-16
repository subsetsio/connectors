-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "PersonalCharacteristics" AS personalcharacteristics,
    "Countries" AS countries,
    "Periods" AS periods,
    "OtherPeople_1" AS otherpeople_1,
    "LegalSystem_2" AS legalsystem_2,
    "Police_3" AS police_3,
    "Politicians_4" AS politicians_4,
    "Parliament_5" AS parliament_5,
    "PoliticalParties_6" AS politicalparties_6,
    "EuropeanParliament_7" AS europeanparliament_7,
    "UnitedNations_8" AS unitednations_8,
    "OtherPeople_9" AS otherpeople_9,
    "LegalSystem_10" AS legalsystem_10,
    "Police_11" AS police_11,
    "Politicians_12" AS politicians_12,
    "Parliament_13" AS parliament_13,
    "PoliticalParties_14" AS politicalparties_14,
    "EuropeanParliament_15" AS europeanparliament_15,
    "UnitedNations_16" AS unitednations_16,
    "PersonalCharacteristics_label" AS personalcharacteristics_label,
    "Countries_label" AS countries_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-80518eng"
