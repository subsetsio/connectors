-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    CAST("Quarter" AS BIGINT) AS quarter,
    "LocationAbbr" AS locationabbr,
    "LocationDesc" AS locationdesc,
    "TopicDesc" AS topicdesc,
    "MeasureDesc" AS measuredesc,
    "DataSource" AS datasource,
    "ProvisionGroupDesc" AS provisiongroupdesc,
    "ProvisionDesc" AS provisiondesc,
    "ProvisionValue" AS provisionvalue,
    "Citation" AS citation,
    CAST("ProvisionAltValue" AS BIGINT) AS provisionaltvalue,
    "DataType" AS datatype,
    "Comments" AS comments,
    "Enacted_Date" AS enacted_date,
    "Effective_Date" AS effective_date,
    "GeoLocation" AS geolocation,
    CAST("DisplayOrder" AS BIGINT) AS displayorder,
    "TopicTypeId" AS topictypeid,
    "TopicId" AS topicid,
    "MeasureId" AS measureid,
    "ProvisionGroupID" AS provisiongroupid,
    CAST("ProvisionID" AS BIGINT) AS provisionid
FROM "cdc-piju-vf3p"
