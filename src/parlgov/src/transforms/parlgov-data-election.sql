SELECT
    CAST(id AS INTEGER)               AS id,
    CAST(date AS DATE)                AS election_date,
    early = 'True'                    AS early,
    CAST(dissolution_date AS DATE)    AS dissolution_date,
    CAST(seats_total AS INTEGER)      AS seats_total,
    CAST(electorate AS BIGINT)        AS electorate,
    CAST(votes_cast AS BIGINT)        AS votes_cast,
    CAST(votes_valid AS BIGINT)       AS votes_valid,
    CAST(country_id AS INTEGER)       AS country_id,
    CAST(type_id AS INTEGER)          AS type_id,
    wikipedia
FROM "parlgov-data-election"
