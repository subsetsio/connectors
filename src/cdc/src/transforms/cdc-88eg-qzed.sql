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
    "Smokefree_Indoor_Air" AS smokefree_indoor_air,
    "Youth_Access" AS youth_access,
    "Licensure" AS licensure,
    "Preemption" AS preemption,
    CAST("PreemptionAltValue" AS BIGINT) AS preemptionaltvalue,
    "GeoLocation" AS geolocation,
    "TopicTypeId" AS topictypeid,
    CAST("TopicId" AS BIGINT) AS topicid,
    "MeasureId" AS measureid
FROM "cdc-88eg-qzed"
