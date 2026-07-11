-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_resource",
    "source_file",
    CAST("InscriptionYear" AS BIGINT) AS inscriptionyear,
    "HusbandAge" AS husbandage,
    "HusbandBirthDate" AS husbandbirthdate,
    "HusbandPreviousMaritalStatus" AS husbandpreviousmaritalstatus,
    "HusbandCityBirthPlace" AS husbandcitybirthplace,
    "HusbandCountryBirthPlace" AS husbandcountrybirthplace,
    "HusbandCityResidencePlace" AS husbandcityresidenceplace,
    "HusbandCountryResidencePlace" AS husbandcountryresidenceplace,
    "HusbandFatherCityResidencePlace" AS husbandfathercityresidenceplace,
    "HusbandFatherCountryResidencePlace" AS husbandfathercountryresidenceplace,
    "HusbandMotherCityResidencePlace" AS husbandmothercityresidenceplace,
    "HusbandMotherCountryResidencePlace" AS husbandmothercountryresidenceplace,
    "HusbandPreviousMarriages" AS husbandpreviousmarriages,
    "HusbandPreviousChildren" AS husbandpreviouschildren,
    "WifeAge" AS wifeage,
    "WifeBirthDate" AS wifebirthdate,
    "WifePreviousMaritalStatus" AS wifepreviousmaritalstatus,
    "WifeCityBirthPlace" AS wifecitybirthplace,
    "WifeCountryBirthPlace" AS wifecountrybirthplace,
    "WifeCityResidencePlace" AS wifecityresidenceplace,
    "WifeCountryResidencePlace" AS wifecountryresidenceplace,
    "WifeFatherCityBirthPlace" AS wifefathercitybirthplace,
    "WifeFatherCountryBirthPlace" AS wifefathercountrybirthplace,
    "WifeMotherCityBirthPlace" AS wifemothercitybirthplace,
    "WifeMotherCountryBirthPlace" AS wifemothercountrybirthplace,
    "WifePreviousMarriages" AS wifepreviousmarriages,
    "WifePreviousChildren" AS wifepreviouschildren,
    "MarriageDate" AS marriagedate,
    "MarriagePlace" AS marriageplace
FROM "instituto-de-estad-sticas-de-puerto-rico-puerto-rico-vital-events-marriages-a"
