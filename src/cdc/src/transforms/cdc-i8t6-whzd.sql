-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    CAST("Quarter" AS BIGINT) AS quarter,
    "LocationAbbr" AS locationabbr,
    "LocationDesc" AS locationdesc,
    "TopicTypeDesc" AS topictypedesc,
    "TopicDesc" AS topicdesc,
    "MeasureDesc" AS measuredesc,
    "Private_Worksites" AS private_worksites,
    "Restaurants" AS restaurants,
    "Bars" AS bars,
    "Type_Of_Restriction" AS type_of_restriction,
    CAST("SummaryAltValue" AS BIGINT) AS summaryaltvalue,
    "Geolocation" AS geolocation,
    "TopicTypeId" AS topictypeid,
    CAST("TopicId" AS BIGINT) AS topicid,
    "MeasureId" AS measureid
FROM "cdc-i8t6-whzd"
