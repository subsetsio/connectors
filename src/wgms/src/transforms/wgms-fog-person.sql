SELECT
    TRY_CAST(id AS BIGINT) AS person_id,
    name,
    surname,
    original_name,
    synonyms,
    orcid,
    url,
    TRY_CAST(birth_year AS INTEGER) AS birth_year,
    TRY_CAST(death_year AS INTEGER) AS death_year,
    remarks
FROM "wgms-fog-person"
