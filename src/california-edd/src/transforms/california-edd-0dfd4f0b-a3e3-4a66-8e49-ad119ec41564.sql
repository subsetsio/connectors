SELECT
    "Area Type" AS area_type,
    "Area Name" AS area_name,
    "Filed week ended" AS filed_week_ended,
    TRY_CAST(NULLIF(regexp_replace(CAST("Initial Claims" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS initial_claims,
    "Reflecting Week Ended" AS reflecting_week_ended,
    TRY_CAST(NULLIF(regexp_replace(CAST("Continued Claims" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS continued_claims,
    TRY_CAST(NULLIF(regexp_replace(CAST("Covered Employment" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS covered_employment,
    TRY_CAST(NULLIF(regexp_replace(CAST("Insured Unemployment Rate" AS VARCHAR), '[^0-9.-]', '', 'g'), '') AS DOUBLE) AS insured_unemployment_rate
FROM "california-edd-0dfd4f0b-a3e3-4a66-8e49-ad119ec41564"
