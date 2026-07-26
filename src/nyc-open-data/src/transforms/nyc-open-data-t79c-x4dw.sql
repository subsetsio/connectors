-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "school_code",
    "school_name",
    "school_type",
    "weighted_register_allocation",
    "weighted_register_allocation_if_fsf_fully_funded",
    "weighted_register_allocation_gap_to_100",
    "funded",
    "foundation_not_included_in_the_funding",
    "collective_bargaining_for_school_based_staff_not_included_in_the_funding",
    "total_fsf_allocation_including_foundation_and_collective_bargaining_costs",
    "total_fsf_allocation_at_100_including_foundation_adjusted_for_collective_bargaining_costs",
    "total_fsf_allocation_gap_to_100_including_foundation_adjusted_for_collective_bargaining_costs",
    "total_budget_allocation",
    "fsf_as_of_total_budget_allocation",
    "nonfsf_budget_allocations"
FROM "nyc-open-data-t79c-x4dw"
