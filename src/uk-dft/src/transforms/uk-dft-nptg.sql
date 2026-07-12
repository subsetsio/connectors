-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "NptgLocalityCode" AS nptglocalitycode,
    "LocalityName" AS localityname,
    "LocalityNameLang" AS localitynamelang,
    "ShortName" AS shortname,
    "ShortNameLang" AS shortnamelang,
    "QualifierName" AS qualifiername,
    "QualifierNameLang" AS qualifiernamelang,
    "QualifierLocalityRef" AS qualifierlocalityref,
    "QualifierDistrictRef" AS qualifierdistrictref,
    "ParentLocalityName" AS parentlocalityname,
    "ParentLocalityNameLang" AS parentlocalitynamelang,
    "AdministrativeAreaCode" AS administrativeareacode,
    CAST("NptgDistrictCode" AS BIGINT) AS nptgdistrictcode,
    "SourceLocalityType" AS sourcelocalitytype,
    "GridType" AS gridtype,
    CAST("Easting" AS BIGINT) AS easting,
    CAST("Northing" AS BIGINT) AS northing,
    CAST("CreationDateTime" AS TIMESTAMP) AS creationdatetime,
    CAST("ModificationDateTime" AS TIMESTAMP) AS modificationdatetime,
    CAST("RevisionNumber" AS BIGINT) AS revisionnumber,
    "Modification" AS modification
FROM "uk-dft-nptg"
