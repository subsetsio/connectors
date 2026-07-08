SELECT
    Company_Phone_Number               AS company_phone_number,
    TRY_CAST(Created_Date AS TIMESTAMP)   AS created_at,
    TRY_CAST(Violation_Date AS TIMESTAMP) AS violation_at,
    Consumer_City                      AS consumer_city,
    Consumer_State                     AS consumer_state,
    Consumer_Area_Code                 AS consumer_area_code,
    Subject                            AS subject,
    Recorded_Message_Or_Robocall       AS robocall,
    CAST(source_file_date AS DATE)     AS source_file_date
FROM "ftc-dnc-reported-call-numbers"
WHERE Company_Phone_Number IS NOT NULL AND Company_Phone_Number <> ''
