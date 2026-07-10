-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Includes State/UT rows and may include an all-India total row; filter to the desired geography level before summing.
SELECT
    "state_ut",
    CAST("no__of_seats" AS BIGINT) AS no_of_seats,
    CAST("constituencies_with_candidates_numbering____1____15" AS BIGINT) AS constituencies_with_candidates_numbering_1_15,
    CAST("constituencies_with_candidates_numbering____15____31" AS BIGINT) AS constituencies_with_candidates_numbering_15_31,
    CAST("constituencies_with_candidates_numbering____31____47" AS BIGINT) AS constituencies_with_candidates_numbering_31_47,
    CAST("constituencies_with_candidates_numbering____47____63" AS BIGINT) AS constituencies_with_candidates_numbering_47_63,
    CAST("constituencies_with_candidates_numbering____63" AS BIGINT) AS constituencies_with_candidates_numbering_63,
    CAST("constituencies_with_candidates_numbering___total_candidates" AS BIGINT) AS constituencies_with_candidates_numbering_total_candidates,
    CAST("candidates_in_a_constituency___min" AS BIGINT) AS candidates_in_a_constituency_min,
    CAST("candidates_in_a_constituency___max" AS BIGINT) AS candidates_in_a_constituency_max,
    CAST("candidates_in_a_constituency___avg" AS BIGINT) AS candidates_in_a_constituency_avg
FROM "election-commission-of-india-0bd877c0-031d-49da-a743-d102dec6e7b7"
