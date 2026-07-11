SELECT
    CAST(id AS INTEGER)       AS id,
    CAST(date AS DATE)        AS change_date,
    party_change,
    name_short,
    name_english,
    name,
    name_ascii,
    name_nonlatin,
    data_source,
    description,
    CAST(party_id AS INTEGER) AS party_id
FROM "parlgov-data-party-name-change"

