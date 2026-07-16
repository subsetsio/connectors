-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Gender" AS gender,
    "Periods" AS periods,
    "TotalDeaths_1" AS totaldeaths_1,
    "DeathsPer1000Inhabitants_2" AS deathsper1000inhabitants_2,
    "StandardisedMortality_3" AS standardisedmortality_3,
    "InfantMortality_4" AS infantmortality_4,
    "InfantMortalityRelative_5" AS infantmortalityrelative_5,
    "DeathsUnder4Weeks_6" AS deathsunder4weeks_6,
    "DeathsUnder4WeeksRelative_7" AS deathsunder4weeksrelative_7,
    "PerinatalMortality24_8" AS perinatalmortality24_8,
    "PerinatalMortality24Relative_9" AS perinatalmortality24relative_9,
    "PerinatalMortality28_10" AS perinatalmortality28_10,
    "PerinatalMortality28Relative_11" AS perinatalmortality28relative_11,
    "LifeExpectancyAtBirth_12" AS lifeexpectancyatbirth_12,
    "AverageAgeAtDeath_13" AS averageageatdeath_13,
    "Gender_label" AS gender_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-37979eng"
