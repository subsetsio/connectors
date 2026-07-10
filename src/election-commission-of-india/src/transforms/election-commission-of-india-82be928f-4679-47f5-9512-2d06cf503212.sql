SELECT
    CAST(party_type AS VARCHAR)                 AS party_type,
    TRY_CAST(no_of_parties_participated AS BIGINT) AS parties_participated
FROM "election-commission-of-india-82be928f-4679-47f5-9512-2d06cf503212"
WHERE party_type IS NOT NULL
