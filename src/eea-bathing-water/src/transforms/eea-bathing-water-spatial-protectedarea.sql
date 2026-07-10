-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Spatial rows describe protected-area designations and can include multiple designations or lifecycle versions for related bathing-water zones.
SELECT
    strptime("beginLifespanVersion", '%Y-%m-%d')::DATE AS beginlifespanversion,
    "countryCode" AS countrycode,
    "cYear" AS cyear,
    strptime("designationPeriodBegin", '%Y-%m-%d')::DATE AS designationperiodbegin,
    strptime("designationPeriodEnd", '%Y-%m-%d')::DATE AS designationperiodend,
    strptime("endLifespanVersion", '%Y-%m-%d')::DATE AS endlifespanversion,
    "inspireIdLocalId" AS inspireidlocalid,
    "inspireIdNamespace" AS inspireidnamespace,
    "inspireIdVersionId" AS inspireidversionid,
    "lat",
    "legalBasisLevel" AS legalbasislevel,
    "legalBasisLink" AS legalbasislink,
    "legalBasisName" AS legalbasisname,
    "link",
    "lon",
    "nameLanguage" AS namelanguage,
    "nameText" AS nametext,
    "nameTextInternational" AS nametextinternational,
    "predecessorsIdentifier" AS predecessorsidentifier,
    "predecessorsIdentifierScheme" AS predecessorsidentifierscheme,
    "relatedZoneIdentifier" AS relatedzoneidentifier,
    "relatedZoneIdentifierScheme" AS relatedzoneidentifierscheme,
    "sizeUom" AS sizeuom,
    "sizeValue" AS sizevalue,
    "specialisedZoneType" AS specialisedzonetype,
    "statusCode" AS statuscode,
    strptime("statusDate", '%Y-%m-%d')::DATE AS statusdate,
    "statusRemarks" AS statusremarks,
    "successorsIdentifier" AS successorsidentifier,
    "successorsIdentifierScheme" AS successorsidentifierscheme,
    "thematicIdIdentifier" AS thematicididentifier,
    "thematicIdIdentifierScheme" AS thematicididentifierscheme,
    "wiseEvolutionType" AS wiseevolutiontype,
    "zoneType" AS zonetype
FROM "eea-bathing-water-spatial-protectedarea"
