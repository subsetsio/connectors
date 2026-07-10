-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Includes State/UT rows and may include an all-India total row; filter to the desired geography level before summing elector counts.
SELECT
    "sl__no_" AS sl_no,
    "state_ut",
    CAST("general_including_nris____m" AS BIGINT) AS electors_general_male,
    CAST("general_including_nris____f" AS BIGINT) AS electors_general_female,
    CAST("general_including_nris____tg" AS BIGINT) AS electors_general_third_gender,
    CAST("general_including_nris____total" AS BIGINT) AS electors_general_total,
    CAST("service___m" AS BIGINT) AS electors_service_male,
    CAST("service___f" AS BIGINT) AS electors_service_female,
    CAST("service___total" AS BIGINT) AS electors_service_total,
    CAST("grand___m" AS BIGINT) AS electors_grand_male,
    CAST("grand___f" AS BIGINT) AS electors_grand_female,
    CAST("grand___tg" AS BIGINT) AS electors_grand_third_gender,
    CAST("grand___total" AS BIGINT) AS electors_grand_total,
    CAST("nris___m" AS BIGINT) AS electors_nri_male,
    CAST("nris___f" AS BIGINT) AS electors_nri_female,
    CAST("nris___tg" AS BIGINT) AS electors_nri_third_gender,
    CAST("nris___total" AS BIGINT) AS electors_nri_total
FROM "election-commission-of-india-1a0a8469-9e7e-4cc7-9f20-5f16ab973cbd"
