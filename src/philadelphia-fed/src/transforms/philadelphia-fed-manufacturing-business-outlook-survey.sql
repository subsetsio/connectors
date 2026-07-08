SELECT CAST(date AS DATE) AS date,
       indicator,
       diffusion_index
FROM "philadelphia-fed-manufacturing-business-outlook-survey"
WHERE diffusion_index IS NOT NULL
ORDER BY date, indicator
