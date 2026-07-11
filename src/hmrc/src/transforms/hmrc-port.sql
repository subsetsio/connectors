SELECT
  CAST(PortId AS INTEGER) AS port_id,
  CAST(PortCodeNumeric AS VARCHAR) AS port_code_numeric,
  CAST(PortCodeAlpha AS VARCHAR) AS port_code_alpha,
  CAST(PortName AS VARCHAR) AS port_name
FROM "hmrc-port"
