SELECT
  name,
  NULLIF(regisration_number, '') AS registration_number,
  CAST(added_date AS DATE) AS added_date,
  CAST(websites AS VARCHAR) AS websites
FROM "bank-negara-malaysia-consumer-alert"
WHERE name IS NOT NULL
