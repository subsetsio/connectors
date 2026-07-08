SELECT
    CAST(id AS INTEGER)               AS id,
    country                           AS country_name_short,
    party_family,
    name_short,
    name_english,
    name,
    name_ascii,
    wikipedia,
    CAST(foundation_date AS DATE)     AS foundation_date,
    CAST(dissolution_date AS DATE)    AS dissolution_date
FROM "parlgov-view-party"
