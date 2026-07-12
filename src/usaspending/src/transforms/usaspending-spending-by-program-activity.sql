SELECT fiscal_year,
       id AS program_activity_id,
       code AS program_activity_code,
       name AS program_activity_name,
       total_obligations
FROM "usaspending-spending-by-program-activity"
