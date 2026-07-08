SELECT
    CAST(state_ut AS VARCHAR)                                            AS state_ut,
    TRY_CAST(no__of_seats AS BIGINT)                                     AS no_of_seats,
    TRY_CAST(constituencies_with_candidates_numbering____1____15 AS BIGINT)  AS constituencies_candidates_1_15,
    TRY_CAST(constituencies_with_candidates_numbering____15____31 AS BIGINT) AS constituencies_candidates_15_31,
    TRY_CAST(constituencies_with_candidates_numbering____31____47 AS BIGINT) AS constituencies_candidates_31_47,
    TRY_CAST(constituencies_with_candidates_numbering____47____63 AS BIGINT) AS constituencies_candidates_47_63,
    TRY_CAST(constituencies_with_candidates_numbering____63 AS BIGINT)       AS constituencies_candidates_63_plus,
    TRY_CAST(constituencies_with_candidates_numbering___total_candidates AS BIGINT) AS total_candidates,
    TRY_CAST(candidates_in_a_constituency___min AS BIGINT)               AS candidates_min,
    TRY_CAST(candidates_in_a_constituency___max AS BIGINT)               AS candidates_max,
    TRY_CAST(candidates_in_a_constituency___avg AS DOUBLE)               AS candidates_avg
FROM "election-commission-of-india-0bd877c0-031d-49da-a743-d102dec6e7b7"
WHERE state_ut IS NOT NULL
