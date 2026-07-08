SELECT
    country_code,
    applicant_name,
    CAST(number_of_applications AS BIGINT) AS number_of_applications
FROM "epo-top-applicants-by-country"
WHERE applicant_name IS NOT NULL AND applicant_name <> ''
