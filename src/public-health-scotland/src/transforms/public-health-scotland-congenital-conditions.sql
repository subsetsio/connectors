-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    CAST("Year" AS BIGINT) AS year,
    "HBR" AS hbr,
    "ConditionGroup" AS conditiongroup,
    CAST("Total" AS BIGINT) AS total,
    "TotalQF" AS totalqf,
    CAST("TotalBirthPopulation" AS BIGINT) AS totalbirthpopulation,
    CAST("TBP" AS DOUBLE) AS tbp,
    "TBPQF" AS tbpqf,
    "Country" AS country,
    "ConditionSubgroup" AS conditionsubgroup,
    "SpecificCondition" AS specificcondition,
    CAST("LiveBirth" AS BIGINT) AS livebirth,
    CAST("SpontaneousStillbirth" AS BIGINT) AS spontaneousstillbirth,
    CAST("SpontaneousLateFetalLoss" AS BIGINT) AS spontaneouslatefetalloss,
    CAST("TOPFA" AS BIGINT) AS topfa,
    CAST("TBPLCI" AS DOUBLE) AS tbplci,
    CAST("TBPUCI" AS DOUBLE) AS tbpuci,
    CAST("LBP" AS DOUBLE) AS lbp,
    CAST("LBPLCI" AS DOUBLE) AS lbplci,
    CAST("LBPUCI" AS DOUBLE) AS lbpuci,
    CAST("TotalExcludingKnownGeneticConditions" AS BIGINT) AS totalexcludingknowngeneticconditions,
    CAST("TBPExcludingKnownGeneticConditions" AS DOUBLE) AS tbpexcludingknowngeneticconditions,
    CAST("TBPExcludingKnownGeneticConditionsLCI" AS DOUBLE) AS tbpexcludingknowngeneticconditionslci,
    CAST("TBPExcludingKnownGeneticConditionsUCI" AS DOUBLE) AS tbpexcludingknowngeneticconditionsuci,
    CAST("LiveBirthPopulation" AS BIGINT) AS livebirthpopulation,
    "ConditionSubgroup2" AS conditionsubgroup2
FROM "public-health-scotland-congenital-conditions"
