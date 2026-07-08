SELECT
    CAST(state_name AS VARCHAR)                AS state_name,
    CAST(constituency_type AS VARCHAR)         AS constituency_type,
    TRY_CAST(no_of_seats AS BIGINT)            AS no_of_seats,
    TRY_CAST(electors___male AS BIGINT)        AS electors_male,
    TRY_CAST(electors___female AS BIGINT)      AS electors_female,
    TRY_CAST(electors___third_gender AS BIGINT) AS electors_third_gender,
    TRY_CAST(electors___total AS BIGINT)       AS electors_total,
    TRY_CAST(electors___nris AS BIGINT)        AS electors_nris,
    TRY_CAST(electors___service AS BIGINT)     AS electors_service,
    TRY_CAST(voters___male AS BIGINT)          AS voters_male,
    TRY_CAST(voters___female AS BIGINT)        AS voters_female,
    TRY_CAST(voters___third_gender AS BIGINT)  AS voters_third_gender,
    TRY_CAST(voters___postal AS BIGINT)        AS voters_postal,
    TRY_CAST(voters___total AS BIGINT)         AS voters_total,
    TRY_CAST(voters___nris AS BIGINT)          AS voters_nris,
    TRY_CAST(voters___poll__ AS DOUBLE)        AS voter_turnout_pct,
    TRY_CAST(rejected_votes__postal_ AS BIGINT) AS rejected_votes_postal,
    TRY_CAST(evm_rejected_votes AS BIGINT)     AS evm_rejected_votes,
    TRY_CAST(nota_votes AS BIGINT)             AS nota_votes,
    TRY_CAST(valid_votes_polled AS BIGINT)     AS valid_votes_polled,
    TRY_CAST(tendered_votes AS BIGINT)         AS tendered_votes
FROM "election-commission-of-india-f7f1bf09-7633-4474-96b2-62630c70f33c"
WHERE state_name IS NOT NULL
