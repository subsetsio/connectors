-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are split by State/UT and constituency type; filter or group constituency_type deliberately before summing turnout measures.
SELECT
    "state_name",
    "constituency_type",
    CAST("no_of_seats" AS BIGINT) AS no_of_seats,
    CAST("electors___male" AS BIGINT) AS electors_male,
    CAST("electors___female" AS BIGINT) AS electors_female,
    CAST("electors___third_gender" AS BIGINT) AS electors_third_gender,
    CAST("electors___total" AS BIGINT) AS electors_total,
    CAST("electors___nris" AS BIGINT) AS electors_nris,
    CAST("electors___service" AS BIGINT) AS electors_service,
    CAST("voters___male" AS BIGINT) AS voters_male,
    CAST("voters___female" AS BIGINT) AS voters_female,
    CAST("voters___third_gender" AS BIGINT) AS voters_third_gender,
    CAST("voters___postal" AS BIGINT) AS voters_postal,
    CAST("voters___total" AS BIGINT) AS voters_total,
    CAST("voters___nris" AS BIGINT) AS voters_nris,
    CAST("voters___poll__" AS DOUBLE) AS voters_poll,
    CAST("rejected_votes__postal_" AS BIGINT) AS rejected_votes_postal,
    CAST("evm_rejected_votes" AS BIGINT) AS evm_rejected_votes,
    CAST("nota_votes" AS BIGINT) AS nota_votes,
    CAST("valid_votes_polled" AS BIGINT) AS valid_votes_polled,
    CAST("tendered_votes" AS BIGINT) AS tendered_votes
FROM "election-commission-of-india-f7f1bf09-7633-4474-96b2-62630c70f33c"
