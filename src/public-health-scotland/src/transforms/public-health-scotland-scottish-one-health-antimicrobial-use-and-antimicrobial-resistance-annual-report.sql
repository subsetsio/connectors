-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "Country" AS country,
    CAST("Year" AS BIGINT) AS year,
    "Organism" AS organism,
    "Antimicrobial" AS antimicrobial,
    "SpecimenType" AS specimentype,
    CAST("NumberTested" AS BIGINT) AS numbertested,
    CAST("Susceptible" AS BIGINT) AS susceptible,
    CAST("SusceptibleAtIncreasedExposure" AS BIGINT) AS susceptibleatincreasedexposure,
    CAST("Resistant" AS BIGINT) AS resistant,
    "CarbapenemaseEnzyme" AS carbapenemaseenzyme,
    "Susceptibility" AS susceptibility,
    "MIC" AS mic,
    CAST("NumberOfIsolates" AS BIGINT) AS numberofisolates,
    CAST("Population" AS BIGINT) AS population,
    CAST("Rate" AS DOUBLE) AS rate
FROM "public-health-scotland-scottish-one-health-antimicrobial-use-and-antimicrobial-resistance-annual-report"
