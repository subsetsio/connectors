-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("ID" AS BIGINT) AS id,
    CAST("IdentificationtoFirstContact (days)" AS BIGINT) AS identificationtofirstcontact_days,
    CAST("IdentificationtoManagerInterview (days)" AS BIGINT) AS identificationtomanagerinterview_days,
    CAST("IdentificationtoObservation (days)" AS BIGINT) AS identificationtoobservation_days,
    CAST("PercentWhoSoughtHealthcare" AS BIGINT) AS percentwhosoughthealthcare,
    "EstablishmentType" AS establishmenttype,
    CAST("Site" AS BIGINT) AS site,
    "FoodPreparationProcess" AS foodpreparationprocess,
    "MenuType" AS menutype,
    "MealsServedDaily" AS mealsserveddaily,
    CAST("FoodIdentified" AS BOOLEAN) AS foodidentified,
    CAST("ContributingFactorIdentified" AS BOOLEAN) AS contributingfactoridentified,
    CAST("AgentIdentified" AS BOOLEAN) AS agentidentified,
    CAST("OnsettoIdentification (days)" AS BIGINT) AS onsettoidentification_days,
    "SampleType" AS sampletype,
    "EpidemiologyInvestigationMethod" AS epidemiologyinvestigationmethod,
    CAST("VisitsforEnvironmentalAssessment" AS BIGINT) AS visitsforenvironmentalassessment
FROM "cdc-x66v-w5ka"
