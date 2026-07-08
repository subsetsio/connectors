SELECT
    "Country"                                                      AS country,
    "ISO2"                                                         AS iso2,
    "ISO3"                                                         AS iso3,
    "Election Type"                                                AS election_type,
    TRY_CAST("Year" AS DATE)                                       AS election_date,
    TRY_CAST(REPLACE(CAST("Voter Turnout" AS VARCHAR), '%', '') AS DOUBLE)          AS voter_turnout_pct,
    TRY_CAST(REPLACE(CAST("Total vote" AS VARCHAR), ',', '') AS BIGINT)             AS total_vote,
    TRY_CAST(REPLACE(CAST("Registration" AS VARCHAR), ',', '') AS BIGINT)           AS registration,
    TRY_CAST(REPLACE(CAST("VAP Turnout" AS VARCHAR), '%', '') AS DOUBLE)            AS vap_turnout_pct,
    TRY_CAST(REPLACE(CAST("Voting age population" AS VARCHAR), ',', '') AS BIGINT)  AS voting_age_population,
    TRY_CAST(REPLACE(CAST("Population" AS VARCHAR), ',', '') AS BIGINT)             AS population,
    TRY_CAST(REPLACE(CAST("Invalid votes" AS VARCHAR), '%', '') AS DOUBLE)          AS invalid_votes_pct,
    "Compulsory voting"                                            AS compulsory_voting
FROM "international-idea-voter-turnout"
WHERE "Country" IS NOT NULL
