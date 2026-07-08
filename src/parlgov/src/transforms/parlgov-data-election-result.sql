SELECT
    CAST(id AS INTEGER)               AS id,
    party_id_source,
    CAST(seats AS INTEGER)            AS seats,
    CAST(vote_share AS DOUBLE)        AS vote_share,
    CAST(votes AS BIGINT)             AS votes,
    CAST(election_id AS INTEGER)      AS election_id,
    CAST(party_id AS INTEGER)         AS party_id,
    CAST(alliance_id AS INTEGER)      AS alliance_id
FROM "parlgov-data-election-result"
