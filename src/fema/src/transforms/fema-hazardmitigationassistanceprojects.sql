-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "region",
    CAST("stateNumberCode" AS BIGINT) AS statenumbercode,
    "state",
    CAST("countyCode" AS BIGINT) AS countycode,
    "county",
    "programArea" AS programarea,
    "projectIdentifier" AS projectidentifier,
    "projectType" AS projecttype,
    "projectCounties" AS projectcounties,
    "numberOfProperties" AS numberofproperties,
    "numberOfFinalProperties" AS numberoffinalproperties,
    "status",
    "subrecipient",
    "projectAmount" AS projectamount,
    CASE WHEN year("initialObligationDate") > 2200 THEN NULL ELSE "initialObligationDate" END AS initialobligationdate,
    "initialObligationAmount" AS initialobligationamount,
    "costSharePercentage" AS costsharepercentage,
    "federalShareObligated" AS federalshareobligated,
    "programFy" AS programfy,
    CASE WHEN year("dateInitiallyApproved") > 2200 THEN NULL ELSE "dateInitiallyApproved" END AS dateinitiallyapproved,
    CASE WHEN year("dateApproved") > 2200 THEN NULL ELSE "dateApproved" END AS dateapproved,
    CASE WHEN year("dateClosed") > 2200 THEN NULL ELSE "dateClosed" END AS dateclosed,
    "recipientTribalIndicator" AS recipienttribalindicator,
    "recipient",
    "disasterNumber" AS disasternumber,
    "benefitCostRatio" AS benefitcostratio,
    "netValueBenefits" AS netvaluebenefits,
    "subrecipientTribalIndicator" AS subrecipienttribalindicator,
    "dataSource" AS datasource,
    "subrecipientAdminCostAmt" AS subrecipientadmincostamt,
    "recipientAdminCostAmt" AS recipientadmincostamt,
    "srmcObligatedAmt" AS srmcobligatedamt
FROM "fema-hazardmitigationassistanceprojects"
