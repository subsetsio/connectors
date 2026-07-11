-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    CAST("InscriptionYear" AS BIGINT) AS inscriptionyear,
    CAST("ControlNumber" AS BIGINT) AS controlnumber,
    "DeceaseGender" AS deceasegender,
    "DeceaseDeathDate" AS deceasedeathdate,
    "DeceaseBirthDate" AS deceasebirthdate,
    "Age" AS age,
    "DeceaseDeathPlace" AS deceasedeathplace,
    "DeceaseCityDeathPlace" AS deceasecitydeathplace,
    "DeceaseCountryDeathPlace" AS deceasecountrydeathplace,
    "DeceaseMaritalStatus" AS deceasemaritalstatus,
    "DeceaseCityResidencePlace" AS deceasecityresidenceplace,
    "DeceaseCountryResidencePlace" AS deceasecountryresidenceplace,
    "DeceaseEducation" AS deceaseeducation,
    "Autopsy" AS autopsy,
    "BirthPlace" AS birthplace,
    "RegistrationDate" AS registrationdate
FROM "instituto-de-estad-sticas-de-puerto-rico-puerto-rico-vital-events-deaths-a"
