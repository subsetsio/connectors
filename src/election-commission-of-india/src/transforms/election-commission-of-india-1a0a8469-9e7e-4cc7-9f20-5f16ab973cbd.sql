SELECT
    CAST(state_ut AS VARCHAR)                          AS state_ut,
    TRY_CAST(general_including_nris____m     AS BIGINT) AS electors_general_male,
    TRY_CAST(general_including_nris____f     AS BIGINT) AS electors_general_female,
    TRY_CAST(general_including_nris____tg    AS BIGINT) AS electors_general_third_gender,
    TRY_CAST(general_including_nris____total AS BIGINT) AS electors_general_total,
    TRY_CAST(service___m     AS BIGINT)                 AS electors_service_male,
    TRY_CAST(service___f     AS BIGINT)                 AS electors_service_female,
    TRY_CAST(service___total AS BIGINT)                 AS electors_service_total,
    TRY_CAST(grand___m     AS BIGINT)                   AS electors_grand_male,
    TRY_CAST(grand___f     AS BIGINT)                   AS electors_grand_female,
    TRY_CAST(grand___tg    AS BIGINT)                   AS electors_grand_third_gender,
    TRY_CAST(grand___total AS BIGINT)                   AS electors_grand_total,
    TRY_CAST(nris___m     AS BIGINT)                    AS electors_nri_male,
    TRY_CAST(nris___f     AS BIGINT)                    AS electors_nri_female,
    TRY_CAST(nris___tg    AS BIGINT)                    AS electors_nri_third_gender,
    TRY_CAST(nris___total AS BIGINT)                    AS electors_nri_total
FROM "election-commission-of-india-1a0a8469-9e7e-4cc7-9f20-5f16ab973cbd"
WHERE state_ut IS NOT NULL
