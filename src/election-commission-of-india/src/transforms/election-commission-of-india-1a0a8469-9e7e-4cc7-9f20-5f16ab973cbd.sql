-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Includes State/UT rows and may include an all-India total row; filter to the desired geography level before summing elector counts.
SELECT
    "sl__no_" AS sl_no,
    "state_ut",
    CAST("general_including_nris____m" AS BIGINT) AS general_including_nris_m,
    CAST("general_including_nris____f" AS BIGINT) AS general_including_nris_f,
    CAST("general_including_nris____tg" AS BIGINT) AS general_including_nris_tg,
    CAST("general_including_nris____total" AS BIGINT) AS general_including_nris_total,
    CAST("service___m" AS BIGINT) AS service_m,
    CAST("service___f" AS BIGINT) AS service_f,
    CAST("service___total" AS BIGINT) AS service_total,
    CAST("grand___m" AS BIGINT) AS grand_m,
    CAST("grand___f" AS BIGINT) AS grand_f,
    CAST("grand___tg" AS BIGINT) AS grand_tg,
    CAST("grand___total" AS BIGINT) AS grand_total,
    CAST("nris___m" AS BIGINT) AS nris_m,
    CAST("nris___f" AS BIGINT) AS nris_f,
    CAST("nris___tg" AS BIGINT) AS nris_tg,
    CAST("nris___total" AS BIGINT) AS nris_total
FROM "election-commission-of-india-1a0a8469-9e7e-4cc7-9f20-5f16ab973cbd"
