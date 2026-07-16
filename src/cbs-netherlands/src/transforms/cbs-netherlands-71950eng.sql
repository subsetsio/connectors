-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Sex" AS sex,
    "AgeAtDecember31" AS ageatdecember31,
    "TypeOfFigure" AS typeoffigure,
    "Periods" AS periods,
    "LifeExpectancy_1" AS lifeexpectancy_1,
    "LifeExpectancyInPerceivedGoodHealth_2" AS lifeexpectancyinperceivedgoodhealth_2,
    "LEWithoutModerateSevereLimitations_3" AS lewithoutmoderateseverelimitations_3,
    "LEWithoutSevereLimitations_4" AS lewithoutseverelimitations_4,
    "LEWithoutLightModerateSevereLim_5" AS lewithoutlightmoderateseverelim_5,
    "LEWithoutChronicMorbidity_6" AS lewithoutchronicmorbidity_6,
    "LEWithoutChrMorbExclHypertension_7" AS lewithoutchrmorbexclhypertension_7,
    "LEWithoutPsychologicalComplaints_8" AS lewithoutpsychologicalcomplaints_8,
    "LifeExpectancyWithoutGALILimitations_9" AS lifeexpectancywithoutgalilimitations_9,
    "LifeExpWithoutSevereGALILimitations_10" AS lifeexpwithoutseveregalilimitations_10,
    "Sex_label" AS sex_label,
    "AgeAtDecember31_label" AS ageatdecember31_label,
    "TypeOfFigure_label" AS typeoffigure_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-71950eng"
