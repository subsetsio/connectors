-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dataSource" AS datasource,
    "courseID" AS courseid,
    "courseCatalogNumber" AS coursecatalognumber,
    CAST("classID" AS BIGINT) AS classid,
    "classStartDatetime" AS classstartdatetime,
    "classEndDatetime" AS classenddatetime,
    "classTimeZone" AS classtimezone,
    "classRegistrationRequired" AS classregistrationrequired,
    "classRegistrationURL" AS classregistrationurl,
    "classRegistrationOpenDate" AS classregistrationopendate,
    "classRegistrationCloseDate" AS classregistrationclosedate,
    "classLocationName" AS classlocationname,
    "classLocationAddress1" AS classlocationaddress1,
    "classLocationAddress2" AS classlocationaddress2,
    "classLocationCity" AS classlocationcity,
    "classLocationState" AS classlocationstate,
    "classLocationZipcode" AS classlocationzipcode,
    "classLocationCounty" AS classlocationcounty,
    "classTrainingProvider" AS classtrainingprovider,
    CAST("classDeliveryMethod" AS BIGINT) AS classdeliverymethod,
    "classPOCName" AS classpocname,
    "classPOCEmail" AS classpocemail,
    CAST("classPOCPhone" AS BIGINT) AS classpocphone,
    "classPOCInfo" AS classpocinfo,
    "classSpecificTitle" AS classspecifictitle,
    "classAdditionalComments" AS classadditionalcomments,
    "id",
    "lastRefresh" AS lastrefresh
FROM "fema-trainingclassschedule"
