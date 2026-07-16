-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Sex" AS sex,
    "Regions" AS regions,
    "Periods" AS periods,
    "PopulationOn1January_1" AS populationon1january_1,
    "PopulationDensity_2" AS populationdensity_2,
    "LiveBornChildren_3" AS livebornchildren_3,
    "LiveBornChildrenRatio_4" AS livebornchildrenratio_4,
    "Deaths_5" AS deaths_5,
    "DeathsRatio_6" AS deathsratio_6,
    "NaturalIncrease_7" AS naturalincrease_7,
    "TotalArrivals_8" AS totalarrivals_8,
    "TotalArrivalsRatio_9" AS totalarrivalsratio_9,
    "DueToImmigration_10" AS duetoimmigration_10,
    "DueToIntermunicipalMoves_11" AS duetointermunicipalmoves_11,
    "TotalDeparturesIncludingAdministra_12" AS totaldeparturesincludingadministra_12,
    "TotalDeparturesIncludingAdmRatio_13" AS totaldeparturesincludingadmratio_13,
    "DueToEmigrationIncludingAdministr_14" AS duetoemigrationincludingadministr_14,
    "NetAdministrativeCorrections_15" AS netadministrativecorrections_15,
    "DueToIntermunicipalMoves_16" AS duetointermunicipalmoves_16,
    "NetMigrationIncludingAdministrative_17" AS netmigrationincludingadministrative_17,
    "PopulationGrowth_18" AS populationgrowth_18,
    "PopulationGrowthRatio_19" AS populationgrowthratio_19,
    "PopulationOn31December_20" AS populationon31december_20,
    "Sex_label" AS sex_label,
    "Regions_label" AS regions_label,
    "Periods_label" AS periods_label
FROM "cbs-netherlands-37259eng"
