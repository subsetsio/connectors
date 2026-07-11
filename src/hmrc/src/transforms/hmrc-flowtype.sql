SELECT
  CAST(FlowTypeId AS SMALLINT) AS flow_type_id,
  CAST(FlowTypeDescription AS VARCHAR) AS flow_type_description
FROM "hmrc-flowtype"
