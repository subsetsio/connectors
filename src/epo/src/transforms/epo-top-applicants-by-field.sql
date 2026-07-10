SELECT
    CAST(field_id AS INTEGER) AS field_id,
    CAST(edition_year AS INTEGER) AS edition_year,
    CAST(rank AS INTEGER) AS rank,
    applicant_name,
    CAST(number_of_applications AS BIGINT) AS number_of_applications
FROM "epo-top-applicants-by-field"
WHERE applicant_name IS NOT NULL AND applicant_name <> ''
