SELECT
  CAST(source_resource_id AS VARCHAR) AS source_resource_id,
  CAST(source_resource_name AS VARCHAR) AS source_resource_name,
  CAST(source_format AS VARCHAR) AS source_format,
  CAST(source_url AS VARCHAR) AS source_url,
  CAST(income_year AS VARCHAR) AS income_year,
  CAST(sheet_name AS VARCHAR) AS sheet_name,
  CAST(row_number AS INTEGER) AS row_number,
  CAST(column_number AS INTEGER) AS column_number,
  CAST(value AS VARCHAR) AS value
FROM "ato-taxation-statistics--financial-ratios-individual"
